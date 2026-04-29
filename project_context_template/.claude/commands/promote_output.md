---
description: Promote durable knowledge from an output file into a wiki page.
argument-hint: "<output-path> <wiki-path>"
---

Read CLAUDE.md.

Promote durable knowledge from output to wiki.

Arguments: $ARGUMENTS

Expected format: `<output-path> <wiki-path>` separated by a space.

If either argument is missing, ask the user before doing anything.

Workflow:

1. Read the output file.
2. Read the target wiki page if it exists.
3. Identify the durable, reusable parts of the output. Strip date-specific narrative, debugging steps, and rejected ideas.
4. Merge into the wiki page using the standard schema. Confirmed facts vs assumptions.
5. Add a link from the wiki page back to the output file as a related raw/output reference.
6. Update `Last updated`.
7. Append a `wiki/log.md` entry: `Promoted <output-path> → <wiki-path>`.

Do not delete the output file. Outputs are immutable history.

If the target wiki page does not exist, create it and link it from `wiki/index.md`.
