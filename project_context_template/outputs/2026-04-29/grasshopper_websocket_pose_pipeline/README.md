# Grasshopper WebSocket Pose Pipeline

Date: 2026-04-29
Execution level: 1, offline only

## Purpose

Prototype a safe Grasshopper-to-WebSocket-to-browser path before connecting the same message schema to ROS2.

```text
Grasshopper/Rhino -> ws://127.0.0.1:8765 -> browser receiver
                                      \
                                       future roslibpy / rosbridge / ROS2 path
```

## Files

- `server.py` starts the WebSocket relay and serves `web_receiver/index.html`.
- `web_receiver/index.html` receives and visualizes the latest pose.
- `send_sample_pose.py` simulates Grasshopper by sending one pose.
- `grasshopper_sender_rhino8.py` is a Rhino 8 ScriptEditor example.
- `roslibpy_pose_publisher_stub.py` shows the next ROS bridge step.
- `smoke_test.py` validates relay ACK and broadcast behavior offline.

## Run

```powershell
cd project_context_template_resilient_handoff_v4\project_context_template\outputs\2026-04-29\grasshopper_websocket_pose_pipeline
python .\server.py
```

Open:

```text
http://127.0.0.1:8000/
```

Send a test pose:

```powershell
python .\send_sample_pose.py
```

Run the smoke test:

```powershell
python .\smoke_test.py
```

## Message Schema

```json
{
  "type": "robot_pose",
  "schema": "cm-itad.ur10e.pose.v1",
  "source": "grasshopper",
  "frame_id": "base",
  "units": {"linear": "m", "angular": "rad"},
  "pose": {
    "position": [0.42, -0.18, 0.36],
    "rotation_vector": [0.0, 3.141593, 0.0]
  },
  "speed": 0.1,
  "acceleration": 0.1
}
```

Translations are meters. Rotations are UR-style axis-angle rotation vectors in radians. Grasshopper millimeters must be converted before sending.

## Grasshopper Options

Use either:

1. Bengesht components:
   - `WS*` with `ws://127.0.0.1:8765`
   - `WS<<` with the JSON payload above
   - optional `WS>>` for ACKs
2. Rhino 8 ScriptEditor:
   - paste `grasshopper_sender_rhino8.py` into a Python component
   - provide `plane`, `send`, and optional `uri` inputs

Legacy GHPython/IronPython should use the Bengesht route first because modern CPython package assumptions do not apply.

## ROS Next Step

When ROS is ready, run a rosbridge server and adapt `roslibpy_pose_publisher_stub.py` to publish `geometry_msgs/PoseStamped` on `/grasshopper/target_pose`.

The current prototype deliberately does not command robot motion.
