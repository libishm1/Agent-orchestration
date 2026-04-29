#!/usr/bin/env python
"""Offline smoke test for the pose relay."""

from __future__ import annotations

import asyncio
import json

try:
    from websockets.asyncio.client import connect as websocket_connect
except ImportError:  # websockets < 14
    from websockets import connect as websocket_connect

from server import PoseHub, websocket_serve
from send_sample_pose import sample_pose


async def main() -> None:
    hub = PoseHub()
    async with websocket_serve(hub.handler, "127.0.0.1", 0) as ws_server:
        port = ws_server.sockets[0].getsockname()[1]
        uri = f"ws://127.0.0.1:{port}"

        async with websocket_connect(uri) as viewer, websocket_connect(uri) as sender:
            viewer_hello = json.loads(await viewer.recv())
            sender_hello = json.loads(await sender.recv())
            assert viewer_hello["type"] == "hello"
            assert sender_hello["type"] == "hello"

            await sender.send(json.dumps(sample_pose()))
            ack = json.loads(await asyncio.wait_for(sender.recv(), timeout=2))
            update = json.loads(await asyncio.wait_for(viewer.recv(), timeout=2))

            assert ack["type"] == "pose_ack", ack
            assert update["type"] == "robot_pose", update
            assert update["pose"]["position"] == [0.42, -0.18, 0.36]
            assert update["frame_id"] == "base"

    print("smoke test passed")


if __name__ == "__main__":
    asyncio.run(main())
