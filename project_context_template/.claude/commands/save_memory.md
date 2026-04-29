---
description: Save the most recent answer to a specific wiki page.
argument-hint: "<wiki-path>"
---

Read CLAUDE.md.

Save durable memory from the most recent assistant answer to: $ARGUMENTS

If `$ARGUMENTS` is empty, ask the user for a path before doing anything.

Rules:

- Save only durable, reusable knowledge. Strip session-specific commentary.
- Preserve the wiki page schema: Purpose, Confirmed facts, Working assumptions, Implementation notes, Code or command patterns, Risks, Open questions, Related raw files, Related wiki pages, Last updated.
- Separate confirmed facts from assumptions. Tag each.
- Add links to related wiki pages and raw files.
- Update `Last updated` to today's date.
- Append a short entry to `wiki/log.md`.

If the target page does not exist, create it with the standard schema and link it in `wiki/index.md` under the appropriate section.

If the target page exceeds 300 lines after the addition, propose a split.
