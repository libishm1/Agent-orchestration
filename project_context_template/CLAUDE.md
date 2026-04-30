# CLAUDE.md

@AGENTS.md

This file imports `AGENTS.md` as the single source of truth for project rules.
Both Codex CLI and Claude Code obey the same rules.
This file adds Claude-Code-specific guidance only.

Last updated: 2026-04-29

## Claude Code specific

### Subagents

Specialist subagents live in `.claude/agents/`. Each has a `description` that triggers proactive delegation.

| Agent | When to delegate | Model |
|---|---|---|
| `wiki-curator` | Ingesting raw → wiki, updating index/log | haiku |
| `health-checker` | Wiki contradictions, orphans, stale claims | haiku |
| `repo-archaeologist` | Inspecting unfamiliar repos before edits | sonnet |
| `robotics-reviewer` | UR10e, RG6, ROS2, URScript, IK/FK code review | sonnet |
| `api-doc-checker` | Verifying current API usage (uses Context7) | sonnet |
| `academic-writer` | Academic writing, thesis drafting, research claims, scholarly argumentation | sonnet |

The parent thread should delegate aggressively. Subagents have their own context windows. Keeping work out of the parent thread is the main reason to use them.

### Slash commands

Reusable prompts live in `.claude/commands/`.

| Command | Purpose |
|---|---|
| `/session_start` | Load index/log/health and summarize state |
| `/ingest_raw` | Pull raw → wiki using wiki-curator |
| `/query_wiki <question>` | Answer using the wiki workflow |
| `/health_check_wiki` | Run health-checker, update health.md |
| `/save_memory <wiki-path>` | Save the last answer to a specific wiki page |
| `/promote_output <output-path> <wiki-path>` | Move durable knowledge from outputs to wiki |
| `/audit_query [flags]` | Query the orchestration audit trail |

### Permissions

`.claude/settings.json` defines tool permissions. Highlights:

- Read/Grep/Glob: any file.
- Write/Edit: `wiki/`, `outputs/`, `.claude/` only.
- Edit/Write to `raw/` is denied.
- Bash is restricted to a small allow-list (git status, git diff, ls, pytest). Anything else requires explicit user approval.

### Imports

Claude Code resolves `@filename` imports inside markdown files. This file imports `AGENTS.md` so any rule update propagates to both Codex and Claude.

## Style

Short declarative sentences. No em dashes. No unsupported claims. State uncertainty clearly.
