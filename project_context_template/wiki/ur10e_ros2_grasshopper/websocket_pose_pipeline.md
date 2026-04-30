# WebSocket Pose Pipeline

## Purpose

Define the Level 1 software pipeline for sending a UR10e with RG6 gripper target pose from Grasshopper/Rhino to a WebSocket relay and receiving it in a browser. This is the dry-run path before publishing the same message to ROS2.

## Confirmed facts

- `websockets` 16.0 is the current API version checked through Context7 on 2026-04-30. Context7 library ID used: `/python-websockets/websockets/16.0`.
- The current `websockets` asyncio server API lives under `websockets.asyncio.server.serve`; top-level `websockets.serve()` aliases the new implementation since version 14.0. Source: https://websockets.readthedocs.io/en/stable/howto/upgrade.html
- The documented WebSocket server pattern is `async def handler(websocket)`, not `handler(websocket, path)`. Use `websocket.request.path` when path access is needed. Source: https://websockets.readthedocs.io/en/stable/reference/asyncio/server.html
- The relay artifact keeps an import fallback because the current local Python environment has `websockets` 11.0.3 installed; new pinned environments should use `websockets.asyncio.*` directly.
- Bengesht provides Grasshopper WebSocket components: `WS*` starts a client connection, `WS<<` sends text, and `WS>>` receives text. Source: https://grasshopperdocs.com/addons/bengesht.html and https://www.food4rhino.com/en/app/bengesht
- RhinoCommon `Rhino.Geometry.Plane` represents an origin and axes in 3D and exposes origin and axis properties. Source: https://developer.rhino3d.com/api/rhinocommon/rhino.geometry.plane
- `roslibpy` connects to ROS through rosbridge over WebSockets and provides topic publish/subscribe, services, parameters, TF client, and actions. PyPI current version checked: 2.0.0, released 2025-10-08. Source: https://pypi.org/project/roslibpy/
- `roslibpy` still describes ROS 2 support as in progress, even though version 2.0.0 added ROS 2 action client support. Treat it as a bridge candidate, not the final ROS2 control layer. Source: https://pypi.org/project/roslibpy/
- Webots R2022b includes Universal Robots UR3e, UR5e, and UR10e models that are described as ROS compatible and include a `toolSlot` field for extending the robot at the end of the arm. Source: https://raw.githubusercontent.com/cyberbotics/webots/R2022b/docs/guide/ure.md
- The referenced third-party UR10e URDF includes the standard UR joint names (`shoulder_pan_joint`, `shoulder_lift_joint`, `elbow_joint`, `wrist_1_joint`, `wrist_2_joint`, `wrist_3_joint`) and `tool0`. Source: https://github.com/Daniella1/urdf_files_dataset/blob/main/urdf_files/ros-industrial/xacro_generated/universal_robots/ur_description/urdf/ur10e.urdf

## Current working assumptions

- Current test path is Level 1 only: no robot, no URSim, no ROS2 motion execution.
- The local WebSocket relay listens on `ws://127.0.0.1:8765`.
- The browser receiver is served from `http://127.0.0.1:8000/`.
- Grasshopper sends a complete pose message, not partial axis values.
- Default pose frame is `base`.
- Translations are meters. Rotations are UR-style axis-angle rotation vectors in radians.
- Grasshopper/Rhino document geometry is in millimeters unless proven otherwise.

## Implementation notes

Prototype artifact:

```text
outputs/2026-04-29/grasshopper_websocket_pose_pipeline/
```

Message schema:

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

Current relay behavior:

- accepts only `type: robot_pose`
- rejects non-meter and non-radian payloads
- rejects non-finite numbers
- applies a loose offline translation sanity bound of +/-2 m
- rejects rotation-vector magnitudes above `2*pi`
- broadcasts accepted pose messages to other connected clients
- sends `pose_ack` to the sender
- never opens UR controller ports and never publishes ROS commands

Grasshopper options:

1. Bengesht route:
   - `WS*`: connect to `ws://127.0.0.1:8765`
   - `WS<<`: send the JSON payload
   - `WS>>`: receive ACK/error messages
2. Rhino 8 ScriptEditor route:
   - use `grasshopper_sender_rhino8.py`
   - input a `Rhino.Geometry.Plane`
   - convert mm to m and plane axes to rotation vector before sending

Context7 status:

- Context7 was available in this Codex session on 2026-04-30.
- `websockets` resolved to `/python-websockets/websockets`; versioned query used `/python-websockets/websockets/16.0`.
- Cached notes were updated in `wiki/local_ai_workflow/websockets_notes.md`.

## Code or command patterns

```powershell
cd project_context_template_resilient_handoff_v4\project_context_template\outputs\2026-04-29\grasshopper_websocket_pose_pipeline
python .\server.py
```

Open the receiver:

```text
http://127.0.0.1:8000/
```

Send a sample pose:

```powershell
python .\send_sample_pose.py
```

Run the offline smoke test:

```powershell
python .\smoke_test.py
```

## Risks

- The Level 1 WebSocket relay is unauthenticated. Bind to localhost only until authentication and network policy are defined.
- Grasshopper solver recomputation can resend poses repeatedly. Gate sends with an explicit `send` boolean, button, data dam, or sequence number.
- Unit mismatch remains the main risk. The relay rejects non-meter payloads, but Grasshopper must still convert from millimeters correctly.
- Axis-angle conversion must be tested with non-trivial rotated planes before ROS publication.
- `roslibpy` is useful for rosbridge experiments, but ROS2 support is not equivalent to a native ROS2 node. Prefer native `rclpy` for the final ROS2 bridge if possible.
- A browser receiver proves transport and schema only. It does not prove kinematic feasibility, collision safety, or controller behavior.

## Open questions

- Should the ROS2 bridge publish `geometry_msgs/PoseStamped`, a custom `TargetPose`, or an action goal?
- Should `frame_id` remain `base`, or should the first ROS bridge use a calibrated `world` frame?
- Should the bridge keep a pose history, or only the latest pose?
- Should the WebSocket server authenticate clients before allowing non-localhost connections?
- Should Grasshopper send pose streams, or only explicit single-shot pose events?

## Related raw files

- `../../../../Robotics in UR Robots_March 2019_r1.pdf`
- `../../../../1-s2.0-S2772991525000040-main.pdf`
- `../../outputs/2026-04-29/reference_cache/polito_38675_tesi.pdf`

## Related wiki pages

- [Overview](overview.md)
- [Architecture](architecture.md)
- [Grasshopper bridge](grasshopper_bridge.md)
- [ROS2 bridge](ros2_bridge.md)
- [Pose and frame rules](pose_frame_rules.md)
- [Testing checklist](testing_checklist.md)
- [Reference digest](reference_digest.md)

## Last updated

2026-04-30
