# raw/00_inbox/

Drop new raw material here when you do not yet know which topic folder it belongs in.

## What goes here

- New meeting notes, conversation pastes, screenshots converted to text.
- Untriaged URLs, bookmarks, and snippets.
- Anything you would otherwise lose.

## What does not go here

- Project-specific raw that clearly belongs in a topic folder. Drop it in the topic folder directly:
  - `raw/ur10e_ros2_grasshopper/`
  - `raw/graphml_baseline_comparison/`
  - `raw/local_ai_codex_claude/`
  - `raw/fabrication_workflows/`
  - `raw/references/`

## Triage

Run `/ingest_raw` (or paste the Codex equivalent prompt). The wiki-curator subagent reads `00_inbox/` first and either summarizes into the relevant wiki page or asks where to file the raw.

## File header

Every new raw file uses this header:

```markdown
# Title

Date:
Source:
Topic:
Status: raw
Do not edit: true
```

Raw files are immutable once written.
