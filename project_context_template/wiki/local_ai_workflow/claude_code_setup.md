# Claude Code Setup

## Purpose

How Claude Code is configured for this project. What it loads automatically from this repo.

## Confirmed facts

- Claude Code reads `CLAUDE.md` from the repository root.
- `CLAUDE.md` imports `AGENTS.md` via the `@AGENTS.md` directive. Both Codex and Claude Code obey the same rules.
- Subagents live in `.claude/agents/`. Each has YAML frontmatter (`name`, `description`, `tools`, `model`).
- Slash commands live in `.claude/commands/`. They support `$ARGUMENTS`.
- Tool permissions live in `.claude/settings.json`. Defaults in this repo: read everything; write to `wiki/`, `outputs/`, `.claude/`; deny writes to `raw/`; restricted Bash allow-list.
- MCP servers (including Context7) configure per the Claude Code docs and the `CONTEXT7_SETUP.md` notes.

## Current working assumptions

- Default model: Sonnet for routine work, Opus for hard reasoning. Subagents pin their own model via the `model:` field.
- The wiki-curator and health-checker subagents run on Haiku to save tokens. The robotics-reviewer, api-doc-checker, and repo-archaeologist run on Sonnet.

## Implementation notes

- Run `/session_start` at the beginning of every session. It loads `wiki/index.md`, the last 5 `wiki/log.md` entries, and `wiki/health.md`.
- Delegate aggressively to subagents. Each subagent runs in its own context window; the parent thread sees only the summary back.
- Subagent descriptions use `MUST BE USED PROACTIVELY` to trigger automatic delegation. If the parent thread keeps doing the work itself, the description is the place to tighten.

## Code or command patterns

```bash
# Start Claude Code in the project root
cd path/to/project
claude

# Verify MCP servers
/mcp

# Daily commands
/session_start
/ingest_raw
/query_wiki <question>
/health_check_wiki
/save_memory <wiki-path>
/promote_output <output-path> <wiki-path>
```

```yaml
# Subagent frontmatter pattern (.claude/agents/*.md)
---
name: <slug>
description: MUST BE USED PROACTIVELY whenever <trigger>. <Short scope statement.>
tools: Read, Grep, Glob   # add Write/Edit/Bash only if needed
model: haiku | sonnet | opus
---
```

## Risks

- **Bash permissions too loose.** A wide-open `Bash(**)` allow defeats the deny-list on `raw/`. Keep Bash restricted.
- **Subagent overuse.** Each invocation has a startup cost. Delegate only when the work is naturally separable.
- **Drift from `AGENTS.md`.** Do not duplicate rules in `CLAUDE.md`. Use the `@AGENTS.md` import.

## Open questions

- Should `repo-archaeologist` run on Haiku for cheap repo scans, with Sonnet reserved for the harder edits? Worth A/B testing.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Codex setup](codex_setup.md)
- [Context7 usage](context7_usage.md)

## Last updated

2026-04-29

## Local model profile

Claude Code can be pointed at a local Anthropic-compatible endpoint. LM Studio is the recommended Windows path for Qwen3-Coder 30B-A3B Q4.

PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:1234"
$env:ANTHROPIC_AUTH_TOKEN = "lmstudio"
claude
```

Bash:

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
claude
```

Use this startup prompt in local-model mode:

```text
You are running in LOCAL MODEL MODE.
Read CLAUDE.md and wiki/index.md.
Do not rely on automatic subagent delegation.
State which specialist role you are using.
Do not scan raw unless explicitly asked.
Keep changes small.
```

Note: Claude subagent `model:` fields such as `haiku` or `sonnet` are cloud-model preferences. A local endpoint may ignore or map them differently. When using Qwen locally, use explicit manual prompts if delegation is unreliable.


## Interchangeable-agent workflow

This setup is designed so Claude Code, Codex, and local Qwen can hand work to each other. The shared state lives in files, not in chat memory.

Before handing off:

1. Save a task plan or checkpoint in `outputs/YYYY-MM-DD/<task_slug>/`.
2. Append a short note to `wiki/log.md`.
3. State the active agent and model used.
4. State whether Context7 was available.
5. List files changed and tests run.

After receiving a handoff:

1. Read `AGENTS.md` or `CLAUDE.md`.
2. Read `wiki/index.md`.
3. Read the latest checkpoint.
4. Continue from the listed next command.

Local models should work from checkpoints. Cloud models should review, plan, and handle high-risk edits.
