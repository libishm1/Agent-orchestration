# raw/references/

External references. Paper PDFs (with notes), datasheet PDFs, vendor docs, useful blog posts and tutorials saved as markdown, GitHub repo notes.

## Rules

- Raw is immutable. Do not edit existing files.
- Add new files only. Use the metadata header below.
- Do not delete files. If a file is wrong, leave it and add a corrective note in the relevant wiki page.

## File header

Every new raw file in this folder uses this header:

```markdown
# Title

Date:
Source:
Topic: references
Status: raw
Do not edit: true
```

## How to ingest

After adding files here, run `/ingest_raw references` (Claude Code) or paste the Codex equivalent prompt with the topic name. The wiki-curator will summarize into the matching `wiki/references/` pages.
