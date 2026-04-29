# Audit Trail Schema

## Purpose

Defines the JSON event types written to `wiki/audit_trail.jsonl`.
One JSON object per line. Append only. Never edit past entries.

## Confirmed facts

Every event shares three required fields:

```
ts        ISO 8601 local datetime  "2026-04-29T14:40:00"
event     string from the list below
agent     string from the agent name list below
```

## Agent names

| Value | Meaning |
|---|---|
| `claude_cloud` | Claude Code with cloud Claude |
| `codex_cloud` | Codex CLI with cloud GPT |
| `qwen_local` | Qwen Code or Claude Code with local Qwen |
| `claude_local` | Claude Code with local model |
| `wiki_curator` | wiki-curator subagent |
| `health_checker` | health-checker subagent |
| `repo_archaeologist` | repo-archaeologist subagent |
| `robotics_reviewer` | robotics-reviewer subagent |
| `api_doc_checker` | api-doc-checker subagent |
| `graphml_reviewer` | graphml-reviewer subagent |
| `local_model_coordinator` | local-model-coordinator subagent |

## Event types

### session_start

```json
{
  "ts": "...",
  "event": "session_start",
  "agent": "...",
  "mode": "cloud | local",
  "files_read": [],
  "open_questions": [],
  "p0_risks": []
}
```

### checkpoint

```json
{
  "ts": "...",
  "event": "checkpoint",
  "agent": "...",
  "task": "task_slug",
  "checkpoint_file": "outputs/YYYY-MM-DD/<slug>/CHECKPOINT_N.md",
  "checkpoint_n": 1,
  "files_read": [],
  "files_changed": [],
  "commands_run": [],
  "outcome": "passed | failed | partial",
  "risks": [],
  "next_prompt": "..."
}
```

### handoff

```json
{
  "ts": "...",
  "event": "handoff",
  "from_agent": "...",
  "to_agent": "...",
  "task": "task_slug",
  "handoff_file": "outputs/YYYY-MM-DD/<slug>/HANDOFF_TO_QWEN.md",
  "stop_conditions": [],
  "files_allowed": []
}
```

### wiki_ingest

```json
{
  "ts": "...",
  "event": "wiki_ingest",
  "agent": "...",
  "task": "task_slug or null",
  "raw_files": [],
  "pages_created": [],
  "pages_updated": [],
  "contradictions": []
}
```

### wiki_update

```json
{
  "ts": "...",
  "event": "wiki_update",
  "agent": "...",
  "task": "task_slug",
  "pages_created": [],
  "pages_updated": [],
  "contradictions": []
}
```

### health_check

```json
{
  "ts": "...",
  "event": "health_check",
  "agent": "...",
  "findings": [
    {"severity": "P0", "page": "wiki/...", "issue": "..."}
  ],
  "p0_count": 0,
  "p1_count": 0,
  "p2_count": 0
}
```

### subagent_call

```json
{
  "ts": "...",
  "event": "subagent_call",
  "agent": "claude_cloud",
  "subagent": "robotics_reviewer",
  "task": "task_slug",
  "delegated_task": "short description",
  "outcome": "complete | blocked | partial"
}
```

### task_complete

```json
{
  "ts": "...",
  "event": "task_complete",
  "agent": "...",
  "task": "task_slug",
  "outcome": "passed | failed",
  "artifacts": [],
  "wiki_pages_promoted": [],
  "open_questions": []
}
```

## Implementation notes

- Use `null` for optional fields that are unknown, not an empty string.
- `task` is a `YYYY-MM-DD/<slug>` path or a bare `<slug>` if date is clear from context.
- `files_read` and `files_changed` use repo-relative paths with forward slashes.
- `ts` is local time. If timezone is known, include offset: `"2026-04-29T14:40:00+03:00"`.

## Related wiki pages

- `wiki/log.md` — narrative session log (human-readable companion)

## Last updated

2026-04-29
