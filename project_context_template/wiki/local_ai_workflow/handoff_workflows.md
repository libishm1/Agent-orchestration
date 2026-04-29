# Handoff Workflows

## Purpose

This page defines the workflow for moving work between Claude Code, Codex, and local Qwen without losing context.

## Confirmed facts

- raw/ is immutable evidence.
- wiki/ is curated memory.
- outputs/ stores generated plans, checkpoints, and handoff notes.
- Claude Code and Codex are preferred for hard planning and review.
- Local Qwen is preferred for offline checkpoint execution.
- Context7 is used for current API compliance, not project memory.

## Current working assumptions

- Local Qwen may be slower and less reliable than cloud Claude or Codex.
- Long work remains possible if divided into checkpoints.
- The handoff layer in outputs/ is the bridge between different agents.

## Workflow

1. Start from wiki/index.md.
2. Create a task plan in outputs/.
3. Split the task into checkpoints.
4. Assign each checkpoint to the appropriate model.
5. Save every checkpoint.
6. Review checkpoints with a stronger cloud model when available.
7. Promote durable knowledge into wiki.

## Agent routing

| Situation | Preferred agent |
|---|---|
| hard planning | Claude Code or Codex cloud |
| current API compliance | Claude Code or Codex with Context7 |
| offline execution | Qwen Code |
| quick local snippet | LM Studio chat |
| robotics safety review | Claude Code with robotics-reviewer |
| GraphML methodology review | Claude Code or Codex cloud |

## Stop conditions

Stop and ask when:

- raw files contradict each other
- robot motion commands would be executed
- package installation is needed
- repo-wide changes exceed the plan
- a file outside allowed directories must be edited
- local Qwen loses track of the task

## Related pages

- local_ai_workflow/agent_mode_matrix.md
- local_ai_workflow/offline_workflow.md
- local_ai_workflow/qwen_code_offline.md
- local_ai_workflow/subagent_routing.md
- project_management/tasks.md

## Last updated

2026-04-29
