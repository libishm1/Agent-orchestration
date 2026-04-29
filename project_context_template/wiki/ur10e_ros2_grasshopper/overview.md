# UR10e ROS2-Grasshopper Overview

## Purpose

High-level map of the UR10e + RG6 + ROS2 + Grasshopper integration. New contributors and new sessions start here. Detailed pages branch off.

## Confirmed facts

- Robot: UR10e with RG6 gripper. Specs in [glossary](../glossary.md) and [pose_frame_rules](pose_frame_rules.md).
- Software stack: ROS2 (Humble or Jazzy), `ur_robot_driver`, `ur_rtde`, MoveIt2, Grasshopper/Rhino 8.
- Two equally valid bridge paths: ROS2 path (`ur_robot_driver` + topic/service bridge) and direct path (`ur_rtde` over RTDE socket).
- Current Level 1 test artifact: `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/`. It sends a Grasshopper-style pose over WebSocket and receives it in a browser. No robot or ROS motion command is issued.

## Current working assumptions

- Default development uses simulation (URSim or MoveIt2 mock hardware) before any hardware connection.
- Rhino document units are millimeters.
- Network: robot IP is on the same LAN segment as the dev machine.

## Implementation notes

- For motion code, start at execution Level 1 (offline). Promote to Level 2 (sim) after unit tests pass. Promote to Level 3 (hardware) only with explicit user approval and a `use_real_hardware` flag.
- Pose conversion is the primary failure source. See [pose_frame_rules](pose_frame_rules.md).
- Use the WebSocket pose pipeline to validate schema, units, and frame tags before connecting the same messages to ROS2.

## Code or command patterns

See linked pages.

## Risks

- Frame confusion. See [pose_frame_rules](pose_frame_rules.md) Risks section.
- Stale URCap or driver versions. See [ros2_bridge](ros2_bridge.md).

## Open questions

See [open_questions](open_questions.md).

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Architecture](architecture.md)
- [ROS2 bridge](ros2_bridge.md)
- [Grasshopper bridge](grasshopper_bridge.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)
- [UR10e RG6 control](ur10e_rg6_control.md)
- [Pose and frame rules](pose_frame_rules.md)
- [Testing checklist](testing_checklist.md)
- [Reference digest](reference_digest.md)

## Last updated

2026-04-29
