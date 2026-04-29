#!/usr/bin/env python
"""Send a sample UR10e pose to the local pose relay."""

from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone

try:
    from websockets.asyncio.client import connect as websocket_connect
except ImportError:  # websockets < 14
    from websockets import connect as websocket_connect


def sample_pose(sequence: int = 1) -> dict:
    return {
        "type": "robot_pose",
        "schema": "cm-itad.ur10e.pose.v1",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "source": "sample_sender",
        "sequence": sequence,
        "frame_id": "base",
        "units": {"linear": "m", "angular": "rad"},
        "pose": {
            "position": [0.42, -0.18, 0.36],
            "rotation_vector": [0.0, 3.141593, 0.0],
        },
        "speed": 0.1,
        "acceleration": 0.1,
    }


async def send(uri: str) -> None:
    async with websocket_connect(uri) as websocket:
        hello = json.loads(await websocket.recv())
        print("connected:", hello["type"], "clients=", hello.get("client_count"))

        await websocket.send(json.dumps(sample_pose()))
        while True:
            reply = json.loads(await websocket.recv())
            print(json.dumps(reply, indent=2))
            if reply.get("type") in {"pose_ack", "pose_error"}:
                break


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uri", default="ws://127.0.0.1:8765")
    args = parser.parse_args()
    asyncio.run(send(args.uri))


if __name__ == "__main__":
    main()
