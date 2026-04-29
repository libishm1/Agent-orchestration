# Offline Workflow

## Purpose

How to keep coding when the lab loses internet, when API quotas run out, or when working from a flight or a low-bandwidth location. The wiki replaces RAG; local models replace cloud agents.

## Confirmed facts

- The wiki is fully readable offline. No external retrieval is needed for project-internal questions.
- Context7 requires internet. When offline, fall back to the cached library notes under `wiki/local_ai_workflow/<library>_notes.md`.
- Local models (LM Studio, Ollama, llama.cpp) provide the agent. See [local_models](local_models.md) for the runtime choice.

## Current working assumptions

- The dev machine has at least one local model pre-pulled before going offline.
- The lab's working repository is a full git clone, not a sparse checkout. All wiki pages are present.
- Cached library notes for the most-used libraries (`ros2`, `ur_rtde`, `fastapi`, `pyg`) exist under `wiki/local_ai_workflow/<library>_notes.md`. Add to the cache during normal online work.

## Implementation notes

Pre-flight checklist before going offline:

- [ ] At least one local model pulled and tested (Ollama: `ollama list`).
- [ ] `wiki/local_ai_workflow/<library>_notes.md` exists for every library you expect to use.
- [ ] The wiki is committed locally (no uncommitted index changes).
- [ ] Last `/health_check_wiki` ran within the past week. Stale entries flagged in `health.md` may be wrong while offline.

In-flight workflow:

1. Point the agent at the local model (LM Studio at `localhost:1234` or Ollama at `localhost:11434`).
2. Use the same wiki commands. The wiki replaces RAG and Context7 for routine questions.
3. When you hit a Context7-only question (e.g. a library you have no notes for), mark the question in `wiki/<topic>/open_questions.md` and resolve it once back online.

Post-flight:

- [ ] Run `/ingest_raw` on any new raw files added offline.
- [ ] Run `/health_check_wiki` to surface stale or contradictory entries.
- [ ] Refresh any library notes that were flagged as questionable.

## Code or command patterns

```bash
# Verify offline-readiness
ollama list
ls wiki/local_ai_workflow/*_notes.md
git status

# Run Claude Code or Codex against a local model
# (use the OpenAI-compatible base URL of LM Studio or Ollama)
export ANTHROPIC_BASE_URL=http://localhost:11434/v1   # for compatible clients
export OPENAI_BASE_URL=http://localhost:1234/v1
```

## Risks

- **Local model tool-use unreliability.** Local models may not call subagents or slash commands reliably. Be prepared to inline the relevant rules manually.
- **Stale wiki.** Working offline against a wiki that has not been health-checked in months can amplify errors. Run a health check before going offline.
- **Library version drift.** Local notes can be older than the installed library. Mark uncertain answers as such in the response.

## Open questions

- Should the lab maintain a regularly-refreshed "offline pack" of cached library notes for the top 10 libraries? Worth scripting.

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Local models](local_models.md)
- [Context7 usage](context7_usage.md)

## Last updated

2026-04-29

## Qwen3-Coder 30B-A3B Q4 offline workflow

Use this workflow when Claude Code or Codex is connected to a local Qwen model.

### Before going offline

- [ ] Qwen3-Coder 30B-A3B Q4 is downloaded and load-tested.
- [ ] A smaller fallback model is downloaded.
- [ ] LM Studio or Ollama starts without internet.
- [ ] The agent can read `AGENTS.md` and `wiki/index.md`.
- [ ] Context7 notes exist for the libraries you expect to touch.
- [ ] `wiki/health.md` has no unresolved P0 contradictions.

### During local-model work

Use this preface:

```text
You are running in LOCAL MODEL MODE.
Use wiki-first workflow.
Read AGENTS.md and wiki/index.md.
Read only relevant wiki pages.
Do not scan raw unless explicitly asked.
Do not edit raw.
Make one focused change at a time.
```

For code edits:

```text
First produce a plan.
Then produce the smallest patch.
Then summarize the diff.
Do not do a multi-file refactor unless I ask.
```

### After coming back online

- [ ] Run `/health_check_wiki`.
- [ ] Refresh stale API claims with Context7.
- [ ] Promote useful offline outputs into wiki pages.
- [ ] Re-run tests with the cloud model if the patch touches robot control logic.


## Offline long-work loop

Use this loop when travelling or working during an outage.

```text
Session start
  -> read index/log/health
  -> pick one task slug
  -> read PLAN.md or create it
  -> do one chunk
  -> write checkpoint
  -> stop or continue
```

Never rely on chat history alone. The checkpoint file is the memory.

## Reconnection loop

When internet returns:

1. Ask Claude cloud or Codex cloud to read the latest checkpoint.
2. Ask for a review of the local model's diff.
3. Use Context7 to verify API-sensitive code.
4. Promote confirmed knowledge to wiki.
5. Update `wiki/log.md`.

This turns offline local work into reviewed project progress.


## Default offline agent

Default to Qwen Code when the internet is unavailable or Claude/Codex limits block work.

Use this order:

1. Qwen Code with local Qwen model.
2. Claude Code pointed to LM Studio if Anthropic-compatible local mode is stable.
3. LM Studio chat with prompts from `outputs/.../QWEN_PROMPT_N.md`.

Offline work must use checkpoint files. The goal is continuity, not cloud-level autonomy.

See `wiki/local_ai_workflow/qwen_code_offline.md`.
