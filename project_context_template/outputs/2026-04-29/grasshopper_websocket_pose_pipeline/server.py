#!/usr/bin/env python
"""Local WebSocket relay for UR10e pose messages.

Execution level: 1, offline only. This server never connects to robot hardware.
It accepts pose JSON from Grasshopper or a test sender and broadcasts the latest
validated pose to every connected browser/client.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import signal
import threading
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

try:
    from websockets.asyncio.server import serve as websocket_serve
except ImportError:  # websockets < 14
    from websockets import serve as websocket_serve


SCHEMA = "cm-itad.ur10e.pose.v1"
DEFAULT_WS_HOST = "127.0.0.1"
DEFAULT_WS_PORT = 8765
DEFAULT_HTTP_HOST = "127.0.0.1"
DEFAULT_HTTP_PORT = 8000
MAX_ABS_TRANSLATION_M = 2.0
MAX_ROTATION_VECTOR_NORM_RAD = 2.0 * math.pi + 1e-6


class PoseValidationError(ValueError):
    """Raised when an incoming pose message is not safe to accept."""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _as_float_list(value: Any, length: int, field_name: str) -> list[float]:
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise PoseValidationError(f"{field_name} must be a list of {length} numbers")

    result: list[float] = []
    for index, item in enumerate(value):
        try:
            number = float(item)
        except (TypeError, ValueError) as exc:
            raise PoseValidationError(f"{field_name}[{index}] is not numeric") from exc
        if not math.isfinite(number):
            raise PoseValidationError(f"{field_name}[{index}] is not finite")
        result.append(number)
    return result


def _extract_pose(event: dict[str, Any]) -> tuple[list[float], list[float]]:
    pose = event.get("pose")
    if isinstance(pose, dict):
        position = _as_float_list(pose.get("position"), 3, "pose.position")
        rotation_vector = _as_float_list(
            pose.get("rotation_vector"), 3, "pose.rotation_vector"
        )
        return position, rotation_vector

    if isinstance(pose, (list, tuple)):
        values = _as_float_list(pose, 6, "pose")
        return values[:3], values[3:]

    raise PoseValidationError(
        "pose must be either [x,y,z,rx,ry,rz] or "
        '{"position":[x,y,z],"rotation_vector":[rx,ry,rz]}'
    )


def normalize_pose_event(raw_message: str) -> dict[str, Any]:
    try:
        event = json.loads(raw_message)
    except json.JSONDecodeError as exc:
        raise PoseValidationError(f"invalid JSON: {exc.msg}") from exc

    if not isinstance(event, dict):
        raise PoseValidationError("message must be a JSON object")

    message_type = event.get("type")
    if message_type != "robot_pose":
        raise PoseValidationError('type must be "robot_pose"')

    units = event.get("units", {})
    linear_unit = units.get("linear", "m") if isinstance(units, dict) else None
    angular_unit = units.get("angular", "rad") if isinstance(units, dict) else None
    if linear_unit != "m":
        raise PoseValidationError('units.linear must be "m"; convert mm before sending')
    if angular_unit != "rad":
        raise PoseValidationError('units.angular must be "rad"')

    position, rotation_vector = _extract_pose(event)

    if any(abs(value) > MAX_ABS_TRANSLATION_M for value in position):
        raise PoseValidationError(
            f"translation exceeds {MAX_ABS_TRANSLATION_M:g} m offline sanity bound"
        )
    rotation_norm = math.sqrt(sum(component * component for component in rotation_vector))
    if rotation_norm > MAX_ROTATION_VECTOR_NORM_RAD:
        raise PoseValidationError("rotation vector magnitude exceeds 2*pi radians")

    frame_id = str(event.get("frame_id", "base"))
    source = str(event.get("source", "unknown"))

    normalized = {
        "type": "robot_pose",
        "schema": SCHEMA,
        "timestamp": str(event.get("timestamp") or utc_now_iso()),
        "source": source,
        "frame_id": frame_id,
        "units": {"linear": "m", "angular": "rad"},
        "pose": {
            "position": position,
            "rotation_vector": rotation_vector,
        },
        "safety": {
            "execution_level": 1,
            "hardware_enabled": False,
            "note": "offline relay only; no robot motion command is issued",
        },
    }

    for optional_key in ("speed", "acceleration", "sequence"):
        if optional_key in event:
            normalized[optional_key] = event[optional_key]

    return normalized


class PoseHub:
    def __init__(self) -> None:
        self.clients: set[Any] = set()
        self.latest_pose: dict[str, Any] | None = None

    async def handler(self, websocket: Any, path: str | None = None) -> None:
        self.clients.add(websocket)
        remote = getattr(websocket, "remote_address", None)
        await self._send(
            websocket,
            {
                "type": "hello",
                "schema": SCHEMA,
                "timestamp": utc_now_iso(),
                "client_count": len(self.clients),
                "latest_pose": self.latest_pose,
            },
        )

        try:
            async for raw_message in websocket:
                await self._handle_message(websocket, raw_message, remote)
        finally:
            self.clients.discard(websocket)

    async def _handle_message(
        self, websocket: Any, raw_message: str, remote: Any
    ) -> None:
        try:
            pose_event = normalize_pose_event(raw_message)
        except PoseValidationError as exc:
            await self._send(
                websocket,
                {
                    "type": "pose_error",
                    "schema": SCHEMA,
                    "timestamp": utc_now_iso(),
                    "error": str(exc),
                },
            )
            return

        self.latest_pose = pose_event
        await self._send(
            websocket,
            {
                "type": "pose_ack",
                "schema": SCHEMA,
                "timestamp": utc_now_iso(),
                "status": "accepted",
                "client_count": len(self.clients),
            },
        )
        await self.broadcast(pose_event, exclude=websocket)
        print(
            f"[pose] from={pose_event['source']} remote={remote} "
            f"frame={pose_event['frame_id']} xyz={pose_event['pose']['position']}"
        )

    async def broadcast(self, event: dict[str, Any], exclude: Any | None = None) -> None:
        stale_clients = []
        for client in list(self.clients):
            if client is exclude:
                continue
            try:
                await self._send(client, event)
            except Exception:
                stale_clients.append(client)
        for client in stale_clients:
            self.clients.discard(client)

    @staticmethod
    async def _send(websocket: Any, event: dict[str, Any]) -> None:
        await websocket.send(json.dumps(event, separators=(",", ":")))


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


def start_http_server(directory: Path, host: str, port: int) -> ThreadingHTTPServer:
    handler = partial(QuietHTTPRequestHandler, directory=str(directory))
    httpd = ThreadingHTTPServer((host, port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


async def run_websocket_server(host: str, port: int) -> None:
    hub = PoseHub()
    async with websocket_serve(hub.handler, host, port):
        print(f"WebSocket relay listening on ws://{host}:{port}")
        await asyncio.Future()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ws-host", default=DEFAULT_WS_HOST)
    parser.add_argument("--ws-port", type=int, default=DEFAULT_WS_PORT)
    parser.add_argument("--http-host", default=DEFAULT_HTTP_HOST)
    parser.add_argument("--http-port", type=int, default=DEFAULT_HTTP_PORT)
    parser.add_argument(
        "--web-dir",
        default=str(Path(__file__).with_name("web_receiver")),
        help="directory containing index.html",
    )
    parser.add_argument("--no-http", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    httpd: ThreadingHTTPServer | None = None
    if not args.no_http:
        web_dir = Path(args.web_dir).resolve()
        httpd = start_http_server(web_dir, args.http_host, args.http_port)
        print(f"Web receiver available at http://{args.http_host}:{args.http_port}/")

    if os.name == "nt":
        asyncio.run(run_websocket_server(args.ws_host, args.ws_port))
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for signame in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(getattr(signal, signame), loop.stop)
    try:
        loop.run_until_complete(run_websocket_server(args.ws_host, args.ws_port))
    finally:
        if httpd:
            httpd.shutdown()
        loop.close()


if __name__ == "__main__":
    main()
