# Subagent Routing

## Purpose

This page defines how Claude Code, Codex, and Qwen Code divide work between specialist agents or specialist role prompts.

## Confirmed facts

Claude Code can use custom subagents from `.claude/agents/`. Use proactive descriptions so Claude delegates before the main context fills.

Codex and Qwen Code should be treated as explicit-routing tools. Ask them to use subagents or role passes directly. Do not rely on silent auto-delegation.

Local Qwen may not provide the same isolated context behavior as Claude Code. Use checkpointed prompts to simulate subagents when offline.

## Routing table

| Trigger | Claude Code route | Codex/Qwen Code route | Output |
|---|---|---|---|
| Old repo, unclear files | repo-archaeologist | Role pass: repo archaeologist | file map + plan |
| UR10e/RG6/ROS2/Grasshopper | robotics-reviewer | Role pass: robotics reviewer | risk list + safe patch plan |
| Current library/API docs | api-doc-checker + Context7 | Context7 if online, local wiki if offline | API pattern + test command |
| DGL/PyG/SVM comparison | graphml-reviewer | Role pass: GraphML reviewer | comparison risks + reproducibility gaps |
| Wiki ingest | wiki-curator | Wiki-curator role prompt | updated index/log/pages |
| Wiki contradictions | health-checker | Health-checker role prompt | updated health.md |
| Local/offline long task | local-model-coordinator | Local-model coordinator role prompt | PLAN.md + CHECKPOINT_N.md |

## Codex prompt

```text
Use subagents first. Do not edit yet.

Subagent 1: repo archaeologist. Find relevant files and old implementations.
Subagent 2: API doc checker. Use Context7 for current APIs only.
Subagent 3: domain reviewer. Use robotics-reviewer or graphml-reviewer logic.
Subagent 4: local-model coordinator. Break the task into Qwen-safe checkpoints.

Return one compact plan:
1. files to read
2. files to edit
3. risks
4. checkpoint plan
5. smallest test command
```

## Qwen Code offline prompt

```text
Read AGENTS.md.
Read wiki/index.md.
You are offline and using local Qwen.
Use sequential role passes, not real parallel subagents.

Task: [paste task]

Pass 1: repo archaeologist. Identify relevant files.
Pass 2: domain reviewer. Identify risks.
Pass 3: local-model coordinator. Create checkpoints.

Do not edit yet. Save the plan to outputs/YYYY-MM-DD/<task_slug>/PLAN.md.
End with the next prompt to execute checkpoint 1.
```

## Current working assumptions

- Cloud Claude remains the best planner for broad autonomous work.
- Codex cloud is strong for patch generation and review.
- Qwen Code with a local Qwen model is the preferred offline coding path.
- Claude Code with local Qwen is useful when the Anthropic-compatible local endpoint is stable.

## Risks

- Local models may over-read files and lose the task thread. Use checkpoint limits.
- Offline mode cannot call Context7. Mark API-sensitive claims as stale.
- Do not let a local model run package installs or robot motion commands.

## Last updated

2026-04-29
