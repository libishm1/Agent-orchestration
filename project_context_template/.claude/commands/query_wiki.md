---
description: Answer a question using the wiki-first workflow.
argument-hint: "<question>"
---

Read CLAUDE.md.

Question: $ARGUMENTS

Workflow:

1. Read `wiki/index.md`.
2. Read only the relevant wiki pages.
3. Read raw only if the wiki page is missing, stale, or contradictory.
4. Use Context7 only for current external API documentation.
5. Cite local file paths in the answer.
6. If the answer is reusable, save it to `outputs/YYYY-MM-DD/<descriptive-name>.md`.
7. Ask where to save durable memory in the wiki.

Do not invent file paths. If a referenced file does not exist, say so.
