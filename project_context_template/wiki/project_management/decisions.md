# Decisions

## Purpose

Append-only record of project-level decisions. One entry per decision. Do not edit past entries; add follow-up entries to update.

## Decision template

Copy this block when adding a new decision.

```markdown
### YYYY-MM-DD — <short title>

**Context:**
**Options considered:**
**Decision:**
**Rationale:**
**Consequences:**
**Reversal cost:**
**Related wiki pages:**
**Related raw files:**
```

## Decisions

### 2026-04-29 — Single source of truth: AGENTS.md

**Context:** Earlier template had near-duplicate `AGENTS.md` and `CLAUDE.md`. Risk of drift.
**Options considered:**
1. Keep both, sync manually.
2. Make `CLAUDE.md` import `AGENTS.md` via `@AGENTS.md`.
3. Delete `CLAUDE.md` entirely.
**Decision:** Option 2.
**Rationale:** Codex requires `AGENTS.md` at the root. Claude Code requires `CLAUDE.md`. The `@` import lets one file own the rules.
**Consequences:** Future rule updates go in `AGENTS.md` only. `CLAUDE.md` only carries Claude-Code-specific notes (subagents, slash commands, settings.json).
**Reversal cost:** Low. Re-duplicate the content at any time.
**Related wiki pages:** `local_ai_workflow/codex_setup.md`, `local_ai_workflow/claude_code_setup.md`.
**Related raw files:** none.

### 2026-04-29 — Default GraphML framework: PyG

**Context:** Earlier template hard-coded DGL across folder names and rules.
**Options considered:**
1. Stay with DGL.
2. Switch to PyG as default; keep DGL pipeline for legacy comparison.
3. Drop DGL entirely.
**Decision:** Option 2. Folder renamed to `graphml_baseline_comparison`. DGL and PyG pipelines both documented.
**Rationale:** DGL had no major release after late 2024. PyG dominates 2025–2026 AEC GraphML literature. Keeping DGL avoids invalidating prior experiments.
**Consequences:** New experiments default to PyG. Existing DGL code is maintained, not extended.
**Reversal cost:** Medium. Rewriting pipelines costs days.
**Related wiki pages:** `graphml_baseline_comparison/overview.md`, `graphml_baseline_comparison/pyg_pipeline.md`, `graphml_baseline_comparison/dgl_pipeline.md`.
**Related raw files:** none yet.

### 2026-04-29 — Remove `.codex/skills/` folder

**Context:** Earlier template had `.codex/skills/*/SKILL.md` files that mirrored Claude Code subagents.
**Options considered:**
1. Keep them, document that they are reference material to paste manually.
2. Delete them and inline the rules into `AGENTS.md`.
**Decision:** Option 2.
**Rationale:** Codex CLI does not auto-load `.codex/skills/`. The files were dead weight and misleading by symmetry with `.claude/agents/`.
**Consequences:** "When working on robotics" and "When working on GraphML" sections in `AGENTS.md` carry the inlined rules.
**Reversal cost:** Low. Re-extract sections to skill files at any time.
**Related wiki pages:** `local_ai_workflow/codex_setup.md`.
**Related raw files:** none.

### 2026-04-29 - Use a Level 1 WebSocket pose relay before ROS2 execution

**Context:** The project needs to test Grasshopper pose messaging before connecting messages to ROS2 or robot motion.
**Options considered:**
1. Send directly from Grasshopper to ROS2.
2. Send directly from Grasshopper to URScript or RTDE.
3. Send Grasshopper pose JSON to a local WebSocket relay and browser receiver first.
**Decision:** Option 3 for the current milestone.
**Rationale:** It validates schema, units, frames, connection stability, and Grasshopper triggering behavior without ROS or hardware risk.
**Consequences:** The current artifact lives in `outputs/2026-04-29/grasshopper_websocket_pose_pipeline/`. ROS2 publication is a follow-up after Level 1 checks pass.
**Reversal cost:** Low. The schema can be reused by HTTP, native ROS2, or rosbridge.
**Related wiki pages:** `ur10e_ros2_grasshopper/websocket_pose_pipeline.md`, `ur10e_ros2_grasshopper/grasshopper_bridge.md`, `ur10e_ros2_grasshopper/ros2_bridge.md`.
**Related raw files:** root-level PDFs and external source URLs listed in `ur10e_ros2_grasshopper/reference_digest.md`.
