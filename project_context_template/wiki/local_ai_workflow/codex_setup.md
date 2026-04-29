# Codex Setup

## Purpose

How Codex CLI is configured for this project on Windows and Linux. What Codex does and does not understand about this repo.

## Confirmed facts

- Codex CLI reads `AGENTS.md` from the repository root automatically.
- Codex does **not** have a subagent system. Specialist behavior must be inlined in `AGENTS.md`.
- Codex does **not** have a slash-command system. Reusable prompts must be pasted manually; see `SETUP_PROMPTS.md` for the canonical set.
- Codex's MCP configuration lives in `~/.codex/config.toml` (Linux/macOS) or `C:\Users\<you>\.codex\config.toml` (Windows).
- The project's `.codex/skills/` folder from earlier iterations is **not loaded by Codex automatically**. It has been removed from this template; the relevant rules are inlined in `AGENTS.md` under "When working on robotics" and "When working on GraphML".

## Current working assumptions

- Codex is invoked from the VS Code integrated terminal in this project's root.
- Default model is the latest GPT coding model available in the user's Codex install.
- Context7 MCP is configured per `CONTEXT7_SETUP.md`.

## Implementation notes

- Codex respects `AGENTS.md` rules including hard limits (no `pip install`, no `git push`, no edits to `raw/`). Verify these are honored on first session.
- For routine work, use the Codex prompts in `SETUP_PROMPTS.md` (session start, ingest, query, health check, save memory).
- When Codex needs to call a Claude-Code subagent equivalent, either:
  - Inline the behavior by pasting the relevant `.claude/agents/<name>.md` content as a prompt, or
  - Run that step in Claude Code instead.

## Code or command patterns

```toml
# ~/.codex/config.toml or C:\Users\<you>\.codex\config.toml

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

# Windows fallback if npx is not on PATH
# command = "C:\\Program Files\\nodejs\\npx.cmd"
# args = ["-y", "@upstash/context7-mcp"]
```

```bash
# Start Codex from the project root
cd path/to/project
codex
```

## Risks

- **Implicit `apply_patch` behavior.** Codex defaults to its own diff/patch flow. State this in the prompt: "Show the diff before applying."
- **Codex ignores `.claude/` files.** Do not rely on Claude-specific subagents or commands when running Codex. Inline the rules instead.
- **Stale `AGENTS.md`.** Updating only `CLAUDE.md` does not update Codex behavior. Always edit `AGENTS.md` (the single source of truth).

## Open questions

- Decide on a tested Codex version pin for the lab to standardize on. Some recent Codex releases changed `apply_patch` defaults.

## Related raw files

(populate via `/ingest_raw` or paste the Codex equivalent prompt)

## Related wiki pages

- [Overview](overview.md)
- [Claude Code setup](claude_code_setup.md)
- [Context7 usage](context7_usage.md)

## Last updated

2026-04-29

## Local model profile

Codex can be used with local models through an OpenAI-compatible local server. Keep this as a fallback profile, not the default cloud profile.

Example `~/.codex/config.toml` profile for LM Studio:

```toml
[model_providers.lmstudio]
name = "LM Studio"
base_url = "http://localhost:1234/v1"
wire_api = "chat"
requires_openai_auth = false

[profiles.qwen3-local]
model_provider = "lmstudio"
model = "qwen3-coder-30b-a3b-instruct"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Start Codex with:

```bash
codex --profile qwen3-local
```

If using Ollama and the Codex version supports the OSS provider:

```bash
ollama list
codex --oss
```

Local-model Codex rule: read `AGENTS.md`, read `wiki/index.md`, then keep work to one focused change.


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
