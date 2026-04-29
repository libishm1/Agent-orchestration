# Project Wiki System

This wiki manages project context for UR10e ROS2-Grasshopper integration, Graph Machine Learning baseline comparison, local AI workflows, and related computational design and fabrication work.

## Memory layers

### `raw/`

Raw contains immutable source material:
- meeting notes
- pasted conversations
- screenshots converted to notes
- code snippets
- GitHub links
- paper notes
- API notes
- experiment logs
- repair and setup notes

Rules:
- Do not rewrite raw files.
- Do not delete raw files.
- Do not treat raw as final truth.
- If raw contains contradictions, preserve them and resolve them in wiki.

### `wiki/`

Wiki contains curated project memory.

Wiki pages must:
- summarize raw evidence
- link back to raw files when possible
- distinguish confirmed facts from assumptions
- record open questions
- stay short enough to load fully into context (≤ 300 lines)
- not paste full raw content

### `outputs/`

Outputs contain generated answers and artifacts:
- code-review notes
- generated plans
- patch summaries
- experiment summaries
- paper section drafts
- setup guides
- debugging reports

Rules:
- Outputs are not automatic permanent memory.
- If an output contains reusable knowledge, run `/promote_output` to merge it into wiki.
- Important decisions must be copied into `wiki/project_management/decisions.md`.

## Sample gold-standard page

For an example of a fully-detailed wiki page, see `wiki/ur10e_ros2_grasshopper/pose_frame_rules.md`. New pages should aim for that level of structure and clarity.

## Maintenance

Run `/health_check_wiki` weekly. Read `wiki/health.md` to see contradictions, orphans, and stale entries.
