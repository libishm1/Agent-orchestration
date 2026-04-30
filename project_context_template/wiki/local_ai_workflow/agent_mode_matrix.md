# Agent Mode Matrix

## Purpose

This page explains how to use Claude Code, Codex, Gemini, and local Qwen models interchangeably without losing project continuity.

## Confirmed facts

- The repository workflow is shared across tools.
- `AGENTS.md` is the single source of truth for project rules.
- `CLAUDE.md` imports `AGENTS.md` and adds Claude Code-specific behavior.
- Claude Code has subagents and slash commands.
- Codex follows `AGENTS.md` and uses prompt workflows rather than Claude slash commands.
- Gemini reads `GEMINI.md`, then follows `AGENTS.md` for shared project rules.
- Local models should use the same wiki-first workflow with smaller context windows and more checkpoints.

## Current working assumptions

- Claude cloud models are best for hard reasoning, subagent-heavy work, and large codebase edits.
- Codex cloud is useful as a second coding agent and for patch-oriented development.
- Gemini cloud is useful for long-context inspection, summarization, contradiction scanning, and documentation drafts.
- Qwen3-Coder 30B-A3B Q4 is the serious offline assistant. It is useful for continuity during travel, outages, and limited connectivity.
- Local Qwen can support long work when the task is checkpointed into files. It should not be asked to hold the whole task in memory.

## Mode table

| Mode | Entry point | Reads | Writes | Best tasks | Avoid |
|---|---|---|---|---|---|
| Claude cloud | Claude Code VS Code or CLI | `CLAUDE.md`, wiki, selected files | code, wiki, outputs | high-autonomy edits, subagents, hard debugging | uncontrolled repo-wide edits |
| Codex cloud | Codex VS Code or CLI | `AGENTS.md`, wiki, selected files | code, wiki, outputs | patches, second opinion, PR-style tasks | relying on Claude subagents |
| Gemini cloud | Gemini CLI or web | `GEMINI.md`, `AGENTS.md`, selected files | summaries, docs, proposed wiki text | long-context reads, contradiction scans, handoff drafts | being final authority for safety, dependency, git, or robot decisions |
| Claude local Qwen | Claude Code pointed to LM Studio Anthropic endpoint | `CLAUDE.md`, wiki index, selected pages | small code edits, wiki, outputs | offline work, code review, URScript/Python helpers | large autonomous refactors |
| Codex local Qwen | Codex profile pointed to LM Studio/Ollama OpenAI endpoint | `AGENTS.md`, wiki index, selected pages | small code edits, wiki, outputs | OpenAI-compatible local fallback | tool-heavy tasks without review |

## Switching protocol

When switching from one agent to another:

1. Run session start.
2. State the active mode.
3. Read `wiki/index.md`.
4. Read the last 5 entries of `wiki/log.md`.
5. Read the latest task checkpoint in `outputs/`.
6. Continue from the next action listed in the checkpoint.

## Long-work protocol

Long work is possible with local models when the project state lives in files.

Use this folder pattern:

```text
outputs/YYYY-MM-DD/<task_slug>/
  PLAN.md
  CHECKPOINT_001.md
  CHECKPOINT_002.md
  DIFF_NOTES.md
  FINAL_SUMMARY.md
```

Each checkpoint must include:

```markdown
# Checkpoint N

## Completed

## Files read

## Files changed

## Decisions made

## Risks

## Next command
```

## Practical rule

Use cloud models for hard leaps. Use local Qwen for durable progress.

The right pattern is not one giant local session. The right pattern is many small verified steps with checkpoints.

## Related wiki pages

- [Local models](local_models.md)
- [Offline workflow](offline_workflow.md)
- [Claude Code setup](claude_code_setup.md)
- [Codex setup](codex_setup.md)

## Last updated

2026-04-30


## Qwen Code offline

Use Qwen Code offline when Claude limits expire, Codex is unavailable, internet is unavailable, or travel requires local-only work.

Strengths:

- terminal coding-agent workflow
- local OpenAI-compatible endpoints
- good fit for Qwen models
- works with `AGENTS.md`, wiki, and outputs checkpoint protocol

Constraints:

- no Context7 when offline
- use smaller checkpoints than cloud agents
- do not do broad autonomous refactors without a prior plan

Recommended role:

`Qwen Code offline = execution worker for checkpointed tasks.`
