# How to Use This Repository

This template manages project context for robotics, GraphML, and local AI work.
The goal is to replace ad-hoc retrieval with a curated wiki the assistant can read into context cheaply.

## First time setup

1. Copy this template into your project root.
2. Open the project in VS Code with Claude Code or Codex installed.
3. Run `/session_start` (Claude Code) or paste the session-start prompt from `SETUP_PROMPTS.md` (Codex).
4. Set up Context7 per `CONTEXT7_SETUP.md`.
5. Drop existing notes, conversations, and references into `raw/` under the matching topic folder.
6. Run `/ingest_raw` (Claude Code) or paste the ingest prompt (Codex).

## Daily loop

1. **Open session.** `/session_start` — assistant reads index/log/health.
2. **Drop new evidence into `raw/`.** Meeting notes, paper screenshots, code snippets, URLs.
3. **Ingest periodically.** `/ingest_raw` — assistant promotes raw → wiki.
4. **Ask questions.** `/query_wiki <question>` — assistant answers from wiki, falls back to raw.
5. **Save reusable answers.** `/save_memory <wiki-path>` — assistant promotes the last answer to a wiki page.
6. **Health check weekly.** `/health_check_wiki` — assistant flags contradictions, stale pages, orphans.

## What goes where

| Type of content | Goes in |
|---|---|
| Raw meeting notes, paper screenshots, code snippets, URLs | `raw/<topic>/` |
| Curated, summarized project memory | `wiki/<topic>/` |
| Generated answers, plans, patch summaries | `outputs/YYYY-MM-DD/` |
| Project-wide rules | `AGENTS.md` (read by both Codex and Claude Code via `CLAUDE.md`) |
| Claude-Code-specific config | `CLAUDE.md`, `.claude/` |

## What replaces RAG

The wiki replaces RAG. Each wiki page is hand-curated and small enough to load fully into context. The index lists every page. The agent reads the index first, then reads only the pages relevant to the question. No vector search. No embedding model. No silent retrieval.

This works because:
- Project context is finite. Most projects have under 200 wiki pages.
- The agent navigates by hyperlinks, not similarity.
- Curation forces the user to decide what is durable knowledge.
- Stale entries are visible in `health.md`.

## What Context7 does

Context7 supplies current external API documentation. ROS2, FastAPI, Three.js, PyG, scikit-learn, and similar libraries change. The wiki cannot keep up. Context7 provides current snippets through MCP.

The agent uses Context7 only for external API questions. It does not use Context7 for project history, personal decisions, or experiment notes.

## Subagents (Claude Code only)

Subagents in `.claude/agents/` save context. Each runs in its own window. The parent thread delegates and receives a summary back.

The parent should delegate aggressively. The whole point is to keep the parent thread short.

## Codex notes

Codex CLI does not have a subagent system. It reads `AGENTS.md` and follows the rules inline. The "When working on robotics" and "When working on GraphML" sections in `AGENTS.md` carry the same content that Claude Code's specialist subagents would carry.

## Local model use

For offline work with Qwen3-Coder 30B-A3B Q4, read `LOCAL_MODEL_SETUP.md` first. Then run `/local_model_session` in Claude Code or use the local-model preface from `wiki/local_ai_workflow/local_models.md` in Codex.


## Using Claude, Codex, and local Qwen together

Use the same repo with all agents. The handoff state lives in files.

- Claude Code cloud: best for subagents, hard debugging, and large reasoning.
- Codex cloud: best for patch-oriented code work and second opinions.
- Local Qwen: best for travel, outages, offline code review, and focused edits.

For any long local task, create a task slug and run:

```text
/local_long_task <task-slug>
```

or paste the "Local long task" prompt from `SETUP_PROMPTS.md` in Codex.

When you return online, ask a cloud model to review the latest checkpoint before merging or promoting memory.


## Qwen Code offline

When you are offline, use Qwen Code as the main local coding agent. Start your local model server first, then launch Qwen Code inside the project folder.

Use the prompt in `wiki/local_ai_workflow/qwen_code_offline.md`.

Qwen Code should read `AGENTS.md`, then `wiki/index.md`, then the latest checkpoint. It should complete one checkpoint at a time and save progress in `outputs/`.

## Resilient online offline workflow

Use `README_HANDOFF_WORKFLOWS.md` when switching between Claude Code, Codex, and local Qwen.

Recommended sequence:

1. Run `/session_start`.
2. Use cloud Claude or Codex to create a plan.
3. Run `/handoff_to_qwen <task>` before travel or offline work.
4. Use Qwen Code to complete one checkpoint at a time.
5. Run `/handoff_to_cloud <checkpoint>` when internet or cloud limits return.
6. Promote durable findings to wiki.
