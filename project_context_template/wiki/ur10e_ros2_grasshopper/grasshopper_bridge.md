# Grasshopper Bridge

## Purpose

How Grasshopper sends toolpaths and commands to the robot, and how it receives state back.

## Confirmed facts

- Four viable bridge styles for this stack:
  1. **Direct URScript over TCP 30002.** Grasshopper opens a socket to the controller, sends URScript text. Simplest. Works without ROS2.
  2. **`ur_rtde` via Python wrapper.** Grasshopper ScriptEditor (CPython 3) imports `ur_rtde`. Bidirectional, low latency.
  3. **HTTP bridge to ROS2.** Grasshopper sends JSON to a FastAPI endpoint that publishes to ROS2 topics. Highest abstraction, ROS2 ecosystem benefits.
  4. **WebSocket relay.** Grasshopper sends pose JSON to a local WebSocket server. Current Level 1 prototype receives the pose in a browser and later can forward to ROS2.
- Existing community options: HAL Robotics, KUKA|prc (KUKA only), Robots plugin (visose/Robots), COMPAS FAB. See `wiki/local_ai_workflow/` and `wiki/project_management/decisions.md` for the comparison.
- Bengesht provides Grasshopper WebSocket client components: `WS*` for connection start, `WS<<` for send, and `WS>>` for receive.

## Current working assumptions

- Current test bridge: local WebSocket relay in `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/`. Grasshopper sends JSON, the server validates and broadcasts to the web receiver. No motion execution.
- Earlier default candidate: FastAPI HTTP to `ur_rtde` on the dev machine. That remains a later design option after the ROS2 path is decided.
- Grasshopper runtime: ScriptEditor (CPython 3, Rhino 8). Legacy GHPython is supported only as a fallback.
- Document units: millimeters. Convert at the bridge.

## Implementation notes

- Keep the bridge stateless where possible. Each request carries a complete pose or trajectory; the server does not hold motion state.
- Apply the unit assert and bounds check on the server side, not in Grasshopper. The Rhino side cannot be trusted to enforce safety.
- Long trajectories should be sent as a single batched payload, not per-waypoint HTTP calls. Per-waypoint HTTP is slow and brittle.
- For the WebSocket path, send explicit events only. Do not stream every Grasshopper recompute unless a rate limiter and sequence gate are in place.
- Prefer JSON arrays of floats over URScript pose strings at the WebSocket boundary. Convert to URScript `p[...]` only at the final URScript generation boundary if needed.

## Code or command patterns

```python
# Grasshopper ScriptEditor (CPython 3) — send a single waypoint
import urllib.request, json

def send_waypoint(plane, speed=0.1, accel=0.1):
    pose = plane_to_urscript_pose(plane, units_mm=True)  # see pose_frame_rules
    payload = {"pose": pose, "speed": speed, "acceleration": accel}
    req = urllib.request.Request(
        "http://localhost:8000/move_l",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))
```

```python
# FastAPI bridge server — minimal example
from fastapi import FastAPI
from rtde_control import RTDEControlInterface

app = FastAPI()
rtde = RTDEControlInterface("192.168.1.10")

@app.post("/move_l")
def move_l(req: dict):
    pose = parse_urscript_pose(req["pose"])  # implement: 'p[...]' → list
    # apply unit/bounds checks
    rtde.moveL(pose, req["speed"], req["acceleration"])
    return {"status": "ok"}
```

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
  }
}
```

```powershell
cd outputs\2026-04-29\grasshopper_websocket_pose_pipeline
python .\server.py
python .\send_sample_pose.py
```

## Risks

- Sending pose literals as strings invites parsing bugs. Prefer JSON arrays of floats over `'p[x,y,z,...]'` strings.
- Grasshopper's solver can re-trigger HTTP calls on every parameter slider change. Add idempotency or rate limiting on the bridge side.
- Long-running motion (multi-second `moveL`) blocks the FastAPI request thread. Use async or a background worker.
- A local WebSocket relay is not a safety layer. It validates message shape only.
- If the WebSocket server is exposed beyond localhost, authentication and network restrictions are required before any ROS bridge is enabled.

## Open questions

- Should the bridge accept full trajectories (list of waypoints) in one call, or stream waypoints?
- Does Grasshopper need real-time state feedback, or is request/response enough?
- Should Bengesht be the preferred Grasshopper WebSocket sender, or should the project standardize on Rhino 8 ScriptEditor code?

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Pose and frame rules](pose_frame_rules.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [ROS2 bridge](ros2_bridge.md)
- [UR10e RG6 control](ur10e_rg6_control.md)

## Last updated

2026-04-29
