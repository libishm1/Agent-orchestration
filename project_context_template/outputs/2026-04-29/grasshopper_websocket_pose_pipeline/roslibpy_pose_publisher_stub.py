#!/usr/bin/env python
"""Future ROS bridge path: WebSocket pose relay to rosbridge via roslibpy.

This is not part of the offline smoke test. It requires a running rosbridge
server, a ROS graph, and the roslibpy package.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math

try:
    from websockets.asyncio.client import connect as websocket_connect
except ImportError:  # websockets < 14
    from websockets import connect as websocket_connect


def rotvec_to_quaternion(rotvec: list[float]) -> dict[str, float]:
    angle = math.sqrt(sum(component * component for component in rotvec))
    if angle < 1e-12:
        return {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
    axis = [component / angle for component in rotvec]
    half = angle * 0.5
    scale = math.sin(half)
    return {
        "x": axis[0] * scale,
        "y": axis[1] * scale,
        "z": axis[2] * scale,
        "w": math.cos(half),
    }


def pose_event_to_pose_stamped(event: dict) -> dict:
    position = event["pose"]["position"]
    orientation = rotvec_to_quaternion(event["pose"]["rotation_vector"])
    return {
        "header": {
            "frame_id": event.get("frame_id", "base"),
            "stamp": {"sec": 0, "nanosec": 0},
        },
        "pose": {
            "position": {"x": position[0], "y": position[1], "z": position[2]},
            "orientation": orientation,
        },
    }


async def bridge(args: argparse.Namespace) -> None:
    import roslibpy

    ros = roslibpy.Ros(host=args.rosbridge_host, port=args.rosbridge_port)
    ros.run()
    topic = roslibpy.Topic(ros, args.topic, "geometry_msgs/PoseStamped")

    try:
        async with websocket_connect(args.pose_ws_uri) as websocket:
            while True:
                message = json.loads(await websocket.recv())
                if message.get("type") != "robot_pose":
                    continue
                topic.publish(roslibpy.Message(pose_event_to_pose_stamped(message)))
    finally:
        topic.unadvertise()
        ros.terminate()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pose-ws-uri", default="ws://127.0.0.1:8765")
    parser.add_argument("--rosbridge-host", default="127.0.0.1")
    parser.add_argument("--rosbridge-port", type=int, default=9090)
    parser.add_argument("--topic", default="/grasshopper/target_pose")
    args = parser.parse_args()
    asyncio.run(bridge(args))


if __name__ == "__main__":
    main()
