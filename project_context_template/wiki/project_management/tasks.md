# Tasks

## Purpose

Active task list. Done items move to the bottom under "Completed". Date items as they are added and as they close.

## In progress

| Added | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 2026-04-29 | Populate `wiki/local_ai_workflow/<library>_notes.md` for ROS2, ur_rtde, FastAPI, PyG. | Libish | Not started | Cache from Context7 during normal work. |
| 2026-04-29 | Verify the actual TCP offset for the lab's RG6 + custom fingertip configuration. | Libish | Not started | Replace the 159 mm placeholder in `pose_frame_rules.md`. |
| 2026-04-29 | Decide the first ROS2 bridge target message for Grasshopper poses. | Libish | Not started | Options: `PoseStamped`, trajectory action, MoveIt2 goal, or checked custom command. |

## Backlog

| Added | Task | Priority | Notes |
|---|---|---|---|
| 2026-04-29 | Decide on ROS2 distro pin (Humble vs Jazzy) for lab standardization. | M | Affects Python version and several dependencies. |
| 2026-04-29 | Pin a tested Qwen-coder size + quant for offline use. | M | See `wiki/local_ai_workflow/local_models.md`. |
| 2026-04-29 | Resolve Context7 library IDs and populate the cached-ID column in `context7_usage.md`. | L | One-time admin task. |

## Completed

| Closed | Task | Notes |
|---|---|---|
| 2026-04-29 | Patch the project_context_template (single-source-of-truth, proactive subagents, model fields, gold-standard wiki page). | This template. |
| 2026-04-29 | Build Level 1 Grasshopper/WebSocket/browser pose relay prototype. | Artifact: `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/`; smoke test passed. |

## Add new task

```markdown
| YYYY-MM-DD | <task> | <owner> | <status> | <notes> |
```


## Local-model task template

```markdown
### Task slug

Status: planned | active | blocked | done
Active mode: Claude cloud | Codex cloud | Claude local Qwen | Codex local Qwen
Checkpoint folder: outputs/YYYY-MM-DD/<task_slug>/
Context7 available: yes | no

Goal:

Current chunk:

Files in scope:

Files out of scope:

Next command:

Review needed from cloud model: yes | no
```
