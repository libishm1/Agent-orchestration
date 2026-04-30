# Resilient Handoff Workflows

This README explains how to switch between Claude Code, Codex, and local Qwen without losing project context.

The goal is continuity.

Use cloud models for planning, review, and difficult reasoning. Use local Qwen for offline checkpoint execution. Use the wiki as stable memory. Use outputs as the handoff layer.

## Memory structure

```text
raw/       immutable source material
wiki/      curated project memory
outputs/   plans, checkpoints, handoffs, patch notes
AGENTS.md  shared rules for Codex and local agents
CLAUDE.md  imports AGENTS.md and adds Claude Code rules
```

## Agent roles

| Mode | Best use | Avoid |
|---|---|---|
| Claude Code cloud | hard planning, multi-file reasoning, robotics risk review | wasting limits on mechanical ingestion |
| Codex cloud | implementation, PR-style changes, second opinion, tests | unbounded repo exploration without a plan |
| Gemini cloud | long-context reading, repo summarization, contradiction scanning, documentation drafting | being final authority for safety, dependency, git, or robot decisions |
| Qwen Code local | offline edits, checkpoint execution, wiki queries, focused patching | whole-repo autonomous refactors |
| LM Studio chat | emergency fallback, explanation, small snippets | complex tool-heavy work |

## Golden rule

Use the lightest workflow that can safely complete the task. Small tasks do not need handoffs, checkpoints, or wiki updates.

Use the full handoff bundle only for long tasks, agent switching, offline continuation, or high-risk work:

```text
outputs/YYYY-MM-DD/TASK_PLAN.md
outputs/YYYY-MM-DD/CHECKPOINT_001.md
outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md
outputs/YYYY-MM-DD/HANDOFF_TO_CLOUD.md
outputs/YYYY-MM-DD/PATCH_SUMMARY.md
```

For medium tasks, one output summary is usually enough. For small tasks, a diff and verification note are enough.

## Verification contract

Before non-trivial coding work, define:

1. Goal.
2. Expected change.
3. Verification method.
4. Evidence required to claim completion.
5. Stop conditions.

Do not claim completion without evidence. If verification cannot be run, give exact manual verification steps.

## Session start prompt

```text
Read AGENTS.md first.
Read wiki/index.md.
Read the last 5 entries of wiki/log.md.
Read wiki/health.md.
Summarize:
1. active task
2. relevant wiki pages
3. recent checkpoints in outputs/
4. risks or contradictions
5. next safest action
Do not edit yet.
```

## Cloud to Qwen handoff prompt

```text
Read AGENTS.md first.
Prepare a handoff for local Qwen Code.

Task:
[PASTE TASK]

Create:
outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md
outputs/YYYY-MM-DD/TASK_PLAN.md

The handoff must include:
1. objective
2. exact files Qwen should read
3. exact files Qwen may edit
4. files Qwen must not edit
5. relevant wiki pages
6. Context7 findings already checked
7. commands to run offline
8. checkpoint size
9. stop conditions
10. next prompt for Qwen

Do not perform the implementation unless I ask.
```

## Qwen offline execution prompt

```text
Read AGENTS.md first.
Read outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md.
Read outputs/YYYY-MM-DD/TASK_PLAN.md.
Read only the wiki pages and files listed in the handoff.

You are in local Qwen mode.
Complete only the next checkpoint.
Do not do repo-wide exploration.
Do not edit raw/.
Do not install packages.
Do not run robot motion commands.

After work, create:
outputs/YYYY-MM-DD/CHECKPOINT_001.md

Include:
1. what was done
2. files read
3. files changed
4. test command and result
5. unresolved risks
6. exact next prompt to continue
```

## Qwen to cloud review prompt

```text
Read AGENTS.md first.
Review the local Qwen checkpoint.

Files:
- outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md
- outputs/YYYY-MM-DD/TASK_PLAN.md
- outputs/YYYY-MM-DD/CHECKPOINT_001.md
- changed files from the checkpoint

Review for:
1. correctness
2. API compliance
3. robotics safety constraints if relevant
4. missing tests
5. whether wiki memory should be updated

Use Context7 only for API-sensitive claims.
Return:
1. accept as is
2. minor edits needed
3. redo with cloud model
4. wiki updates needed
```

## Claude to Codex handoff prompt

```text
Read AGENTS.md first.
Prepare a Codex handoff.

Task:
[PASTE TASK]

Create outputs/YYYY-MM-DD/HANDOFF_TO_CODEX.md with:
1. objective
2. files to inspect
3. files allowed to edit
4. tests to run
5. known risks
6. expected diff size
7. stop conditions

Codex should use subagents first if repo exploration is needed.
Do not edit yet.
```

## Codex to Claude handoff prompt

```text
Read AGENTS.md first.
Review outputs/YYYY-MM-DD/HANDOFF_TO_CLAUDE.md or the latest Codex checkpoint.

Check:
1. whether the edit matches the plan
2. whether the code violates project rules
3. whether Context7 should refresh any API assumption
4. whether a wiki update is needed
5. whether the task should continue in cloud or local mode
```

## Context7 API compliance prompt

```text
Read AGENTS.md first.
Use Context7 for current API documentation.
Check only the APIs relevant to this task.

Return:
1. current API pattern
2. deprecated or risky pattern
3. minimal code change
4. test command
5. whether to cache the finding in wiki/local_ai_workflow/context7_usage.md
```

## UR10e ROS2 Grasshopper prompt

```text
Read AGENTS.md first.
Use the robotics workflow.

Task:
[PASTE TASK]

Rules:
- never mix TCP poses with motion poses
- preserve URScript p[x, y, z, rx, ry, rz] format
- state whether Grasshopper Python is IronPython 2.7 or CPython 3
- prefer ROS2 conventions
- do not run robot motion commands

If offline, complete one checkpoint only.
Save progress to outputs/YYYY-MM-DD/.
```

## GraphML baseline comparison prompt

```text
Read AGENTS.md first.
Use the GraphML baseline workflow.

Task:
[PASTE TASK]

Check:
1. graph construction
2. dataset split
3. feature set
4. DGL or PyG pipeline
5. SVM baseline fairness
6. metrics
7. random seed
8. reproducibility notes

Save reusable notes to outputs/YYYY-MM-DD/ and suggest wiki updates.
```

## Checkpoint template

```markdown
# CHECKPOINT_N

Date:
Mode: Claude Code / Codex / Qwen Code / LM Studio
Task:

## Objective

## Definition of Done

## Files read

## Files changed

## Commands run

## Result

## Verification evidence

## Risks

## Next step

## Exact continuation prompt
```

## Handoff file template

```markdown
# HANDOFF_TO_AGENT

Date:
From:
To:
Mode:

## Objective

## Current state

## Relevant wiki pages

## Files to read

## Files allowed to edit

## Files forbidden

## Known constraints

## Verification contract

## Commands

## Stop conditions

## Next prompt
```

## Travel and offline checklist

Before travel:

1. Pull latest repo changes.
2. Start a session and run `/session_start`.
3. Create `HANDOFF_TO_QWEN.md` for active tasks.
4. Download needed docs, models, and datasets.
5. Test Qwen Code on one small checkpoint.
6. Confirm outputs path exists for the day.
7. Keep a 7B or 14B fast fallback model installed.

During travel:

1. Use Qwen Code only on checkpoint tasks.
2. Keep context small.
3. Save every result to outputs.
4. Do not do risky package installs.
5. Do not attempt large architectural rewrites.

After travel:

1. Ask Claude or Codex to review checkpoints.
2. Promote durable memory to wiki.
3. Append wiki/log.md.
4. Update wiki/health.md if contradictions appeared.
