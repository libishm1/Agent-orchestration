# raw/graphml_baseline_comparison/

GraphML baseline comparison. Dataset construction notes, IFC-to-graph dumps, DGL/PyG experiment logs, SVM hyperparameter sweeps, evaluation outputs, metric definitions, raw paper notes from the PRISMA review.

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
Topic: graphml_baseline_comparison
Status: raw
Do not edit: true
```

## How to ingest

After adding files here, run `/ingest_raw graphml_baseline_comparison` (Claude Code) or paste the Codex equivalent prompt with the topic name. The wiki-curator will summarize into the matching `wiki/graphml_baseline_comparison/` pages.
