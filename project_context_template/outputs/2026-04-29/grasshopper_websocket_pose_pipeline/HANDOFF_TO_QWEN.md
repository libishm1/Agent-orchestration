# HANDOFF_TO_QWEN

Date: 2026-04-29
From: Codex cloud
To: Local Qwen Code
Mode: focused offline checkpoint

## Objective

Continue testing the Level 1 Grasshopper WebSocket pose pipeline without touching robot hardware.

## Current state

The offline relay and browser receiver are implemented. The Python smoke test passed.

## Relevant wiki pages

- `wiki/ur10e_ros2_grasshopper/websocket_pose_pipeline.md`
- `wiki/ur10e_ros2_grasshopper/grasshopper_bridge.md`
- `wiki/ur10e_ros2_grasshopper/ros2_bridge.md`
- `wiki/ur10e_ros2_grasshopper/testing_checklist.md`
- `wiki/ur10e_ros2_grasshopper/open_questions.md`

## Files to read

- `AGENTS.md`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/README.md`
- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/CHECKPOINT_001.md`

## Files allowed to edit

- `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/*`
- `wiki/ur10e_ros2_grasshopper/websocket_pose_pipeline.md`
- `wiki/ur10e_ros2_grasshopper/testing_checklist.md`

## Files forbidden

- `raw/`
- robot hardware scripts outside the Level 1 output folder

## Known constraints

- Do not install packages.
- Do not run robot motion commands.
- Do not expose the WebSocket relay beyond localhost.

## Commands

```powershell
cd outputs\2026-04-29\grasshopper_websocket_pose_pipeline
python .\smoke_test.py
python .\server.py
```

## Stop conditions

- Any request to command real hardware.
- Any package installation requirement.
- Any contradiction in units, frames, or ROS message type.

## Next prompt

Read `AGENTS.md`, then complete one checkpoint: test the browser receiver and record whether the sample pose appears correctly.
