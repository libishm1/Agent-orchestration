# CHECKPOINT_001

Date: 2026-04-29
Mode: Codex cloud
Task: Level 1 Grasshopper WebSocket pose pipeline

## Objective

Build the offline WebSocket pose relay and promote durable findings to the wiki.

## Files read

- `AGENTS.md`
- `CONTEXT7_SETUP.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/health.md`
- `wiki/local_ai_workflow/context7_usage.md`
- `wiki/ur10e_ros2_grasshopper/overview.md`
- `wiki/ur10e_ros2_grasshopper/architecture.md`
- `wiki/ur10e_ros2_grasshopper/grasshopper_bridge.md`
- `wiki/ur10e_ros2_grasshopper/ros2_bridge.md`
- `wiki/ur10e_ros2_grasshopper/pose_frame_rules.md`
- `wiki/ur10e_ros2_grasshopper/testing_checklist.md`
- `Robotics in UR Robots_March 2019_r1.pdf`
- `1-s2.0-S2772991525000040-main.pdf`
- `outputs/2026-04-29/reference_cache/polito_38675_tesi.pdf`

## Files changed

- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/server.py`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/send_sample_pose.py`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/smoke_test.py`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/grasshopper_sender_rhino8.py`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/roslibpy_pose_publisher_stub.py`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/web_receiver/index.html`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/README.md`
- `wiki/ur10e_ros2_grasshopper/websocket_pose_pipeline.md`
- `wiki/ur10e_ros2_grasshopper/reference_digest.md`
- `wiki/ur10e_ros2_grasshopper/overview.md`
- `wiki/ur10e_ros2_grasshopper/architecture.md`
- `wiki/ur10e_ros2_grasshopper/grasshopper_bridge.md`
- `wiki/ur10e_ros2_grasshopper/ros2_bridge.md`
- `wiki/ur10e_ros2_grasshopper/testing_checklist.md`
- `wiki/ur10e_ros2_grasshopper/open_questions.md`
- `wiki/local_ai_workflow/context7_usage.md`
- `wiki/project_management/decisions.md`
- `wiki/project_management/risks.md`
- `wiki/project_management/tasks.md`
- `wiki/index.md`
- `wiki/log.md`

## Commands run

```powershell
python .\smoke_test.py
```

Result:

```text
smoke test passed
```

## Risks

- Browser receiving validates transport and schema only.
- `roslibpy` is not the final ROS2 control layer until ROS2 behavior is verified.
- Grasshopper solver recomputation must be gated.

## Next step

Run `python .\server.py`, open `http://127.0.0.1:8000/`, then send from Bengesht or `grasshopper_sender_rhino8.py`.

## Exact continuation prompt

Read `AGENTS.md` first. Continue from `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/CHECKPOINT_001.md`. Test the Level 1 WebSocket pose pipeline from Grasshopper, then decide the first ROS2 target message type.
