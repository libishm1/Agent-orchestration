# Local AI Workflow Overview

## Purpose

How agentic coding tools (Codex, Claude Code) are configured for this project, and how they interact with Context7 and local models.

## Confirmed facts

- Two primary agents: **Codex CLI** and **Claude Code**. Both run inside VS Code.
- Codex reads `AGENTS.md` at the repo root.
- Claude Code reads `CLAUDE.md`, which imports `AGENTS.md` via `@AGENTS.md`. Same rules apply to both.
- Context7 is available as an MCP server in both clients. Setup details in `CONTEXT7_SETUP.md`.
- Claude Code has a subagent system (`.claude/agents/`) and a slash command system (`.claude/commands/`). Codex has neither — all guidance is inline in `AGENTS.md`.

## Current working assumptions

- Cloud models: Anthropic Sonnet/Opus for Claude Code, OpenAI GPT for Codex. Local models for offline emergencies.
- Context budget is the binding constraint, not model intelligence. The wiki system exists to keep context tight.

## Implementation notes

- The wiki replaces RAG. The agent navigates the wiki by hyperlinks, not similarity search.
- Subagents (Claude Code) run in their own context windows. Use them aggressively to keep the parent thread short.
- Output files in `outputs/YYYY-MM-DD/` are not permanent memory. Promote to wiki via `/promote_output`.

## Code or command patterns

```bash
# Claude Code from VS Code terminal
claude

# Codex from VS Code terminal
codex
```

```text
# Inside Claude Code, common commands
/session_start
/ingest_raw
/query_wiki <question>
/health_check_wiki
/save_memory <wiki-path>
/promote_output <output-path> <wiki-path>
```

## Risks

- Drift between `AGENTS.md` and `CLAUDE.md`. Mitigation: `CLAUDE.md` imports via `@AGENTS.md`. Do not duplicate content.
- Context7 used as project memory. Mitigation: rules in `AGENTS.md` and the caching strategy in [context7_usage](context7_usage.md).
- Subagent overuse. Each subagent invocation has a startup cost. Use them when the work is naturally separable, not for every small task.

## Open questions

- Pin a tested local model for offline use. Currently leaning Qwen-coder family.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Codex setup](codex_setup.md)
- [Claude Code setup](claude_code_setup.md)
- [Context7 usage](context7_usage.md)
- [Local models](local_models.md)
- [Offline workflow](offline_workflow.md)

## Last updated

2026-04-29
