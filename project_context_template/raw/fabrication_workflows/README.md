# raw/fabrication_workflows/

Computational design and fabrication. Open3D/Depth Anything experiments, Grasshopper Python notes, laser cutting + 3D printing logs, material/tolerance notes, jig and fixture documentation.

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
Topic: fabrication_workflows
Status: raw
Do not edit: true
```

## How to ingest

After adding files here, run `/ingest_raw fabrication_workflows` (Claude Code) or paste the Codex equivalent prompt with the topic name. The wiki-curator will summarize into the matching `wiki/fabrication_workflows/` pages.
