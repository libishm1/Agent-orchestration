# UR10e ROS2-Grasshopper Architecture

## Purpose

Block diagram and subsystem map. How the parts connect. What runs where.

## Confirmed facts

The pipeline has six subsystems. Not all are used in every project:

1. **Design** — Grasshopper/Rhino. Generates geometry and toolpaths.
2. **Bridge** — Middleware translating Grasshopper output into robot-readable commands.
3. **Planning** — MoveIt2 or hand-rolled IK/trajectory generation.
4. **Execution** — `ur_rtde` or `ur_robot_driver` running on the dev machine; URScript on the controller.
5. **Perception** (optional) — Depth camera, SAM, point cloud processing.
6. **Web receiver** (current Level 1 test) - browser page that receives pose JSON over WebSocket for schema and transport validation.

Network:
- Dev machine ↔ UR controller: TCP/IP on the LAN.
- URScript port: 30002 (secondary interface).
- RTDE port: 30004 (real-time data exchange).
- Primary interface: 30001.
- Dashboard server: 29999.
- Level 1 local WebSocket relay: `ws://127.0.0.1:8765`.
- Level 1 browser receiver: `http://127.0.0.1:8000/`.

## Current working assumptions

- Single-machine dev workflow (no separate planning PC).
- ROS2 stack runs in Docker (`network_mode: host` or CycloneDDS unicast peers for cross-host discovery).
- Current test bridge is WebSocket-based for fast browser validation. FastAPI HTTP remains a candidate for request/response commands. ROS2 remains the target integration layer.

## Implementation notes

Current Level 1 architecture:

```text
Grasshopper/Rhino -> local WebSocket relay -> browser receiver
                                  \
                                   future ROS2 bridge
```

The WebSocket relay validates JSON and broadcasts accepted poses. It does not run IK, plan trajectories, publish ROS topics, or command hardware.

## Code or command patterns

```bash
# Quick connectivity check
ping <robot-ip>
nc -zv <robot-ip> 30002  # URScript port
nc -zv <robot-ip> 30004  # RTDE port
```

## Risks

- Network topology assumptions. Parameterize robot IP, ROS_DOMAIN_ID, bridge port.
- Docker `network_mode: host` does not work on Docker Desktop for Windows. Use macvlan or run ROS2 natively on Linux.

## Open questions

- Should planning live on the same machine as Grasshopper, or split across machines?
- Is the bridge stateless (request/response) or stateful (long-lived WebSocket)?
- Should the Level 2 path use URSim, Webots, MoveIt2 mock hardware, or more than one simulator?

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [ROS2 bridge](ros2_bridge.md)
- [Grasshopper bridge](grasshopper_bridge.md)
- [WebSocket pose pipeline](websocket_pose_pipeline.md)

## Last updated

2026-04-29
