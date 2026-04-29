# Open Questions

## Purpose

Track unresolved design choices for the UR10e with RG6 gripper, ROS2, Grasshopper, and WebSocket bridge work.

## Confirmed facts

- Current Level 1 WebSocket prototype exists in `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/`.
- The prototype validates pose JSON and broadcasts to a browser receiver only.
- The prototype smoke test passed on 2026-04-29.

## Current working assumptions

- ROS2 remains the target integration layer.
- The browser receiver is the first receiver because it is low risk and makes payload mistakes visible.
- Level 2 simulation must pass before any hardware work.

## Implementation notes

Keep questions here until resolved in [Decisions](../project_management/decisions.md) or a specific wiki page.

## Code or command patterns

```powershell
python outputs\2026-04-29\grasshopper_websocket_pose_pipeline\smoke_test.py
```

## Risks

- Open questions about frames and ROS message type can lead to incompatible bridge code if left unresolved too long.
- WebSocket transport can appear correct while pose semantics are still wrong.

## Open questions

- What is the authoritative ROS2 distro for this project: Humble or Jazzy?
- Should the Grasshopper sender standard be Bengesht components, Rhino 8 ScriptEditor Python, or both?
- Should the first ROS bridge use native `rclpy` or `roslibpy` through rosbridge?
- Should the first ROS message be `geometry_msgs/PoseStamped`, `trajectory_msgs/JointTrajectory`, a MoveIt2 action goal, or a custom checked command message?
- What is the calibrated transform between Rhino world and UR `base`?
- Should the browser receiver become a 3D URDF viewer, or remain a numeric pose monitor?
- Should Webots be part of Level 2 validation, or should Level 2 standardize on URSim and MoveIt2 mock hardware?
- Should the local PDFs be copied into `raw/references/` with metadata headers?

## Related raw files

(populate via /ingest_raw)

## Related wiki pages

- [Overview](overview.md)
- [Pose and frame rules](pose_frame_rules.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [Reference digest](reference_digest.md)

## Last updated

2026-04-29
