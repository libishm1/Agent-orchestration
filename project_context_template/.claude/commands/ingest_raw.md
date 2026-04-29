---
description: Ingest raw files into the wiki using the wiki-curator subagent.
argument-hint: "[optional: topic folder, e.g. ur10e_ros2_grasshopper]"
---

Read CLAUDE.md.

Delegate to the `wiki-curator` subagent.

Task:
Ingest raw material into wiki.
Topic filter: $ARGUMENTS

If no topic was provided, ingest from `raw/00_inbox/` first.

Rules:
- Do not edit `raw/`.
- Read `wiki/index.md` first.
- Process up to 5 raw files per pass.
- Create or update only relevant wiki pages.
- Keep wiki pages under 300 lines.
- Separate confirmed facts from assumptions.
- Update `wiki/health.md` with contradictions tagged P0/P1/P2.
- Append to `wiki/log.md`.

At the end, report:

1. Files created
2. Files updated
3. Contradictions
4. Open questions
5. Next recommended ingest task
