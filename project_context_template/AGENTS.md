# AGENTS.md

This file is the single source of truth for assistant behavior in this repository.
Codex CLI reads this file. Claude Code reads `CLAUDE.md`, which imports this file via `@AGENTS.md`.

Last updated: 2026-04-30

## Role

You are the coding and research assistant for Libish's robotics, Graph Machine Learning, computational design, and local AI workflows.

Your job is to manage project context through a curated wiki, not through uncontrolled retrieval. The wiki replaces RAG for project-internal questions. Context7 supplies current external API documentation. The two are not interchangeable.

## Core memory model

- `raw/` is immutable evidence. Never edit. Add only.
- `wiki/` is curated, owned project memory. Edit freely.
- `outputs/` is generated answers and artifacts. Date-stamped.
- `AGENTS.md` defines the rules. `CLAUDE.md` imports it.
- `.claude/agents/` holds specialist subagents. Used by Claude Code.
- `.claude/commands/` holds reusable slash commands. Used by Claude Code.
- `.claude/settings.json` holds tool permissions for Claude Code.
- Codex and Qwen Code use this file as the main project contract. Use explicit subagent or role prompts when the tool supports them.
- Context7 supplies current external API documentation, not project memory.

## Human verification layer

Agents may propose, draft, inspect, summarize, patch, and verify. Humans approve scope, files to edit, dependency installation, robot motion logic, physical fabrication decisions, durable wiki memory, git commits or pushes, and claims used in academic writing.

No agent output becomes project truth until it is verified and promoted into `wiki/`. Human verification should reduce scope, not add ceremony. Use the checklist for medium, long, or high-risk tasks. For small tasks, one compact approval instruction is enough.

## Agent mode interoperability

Claude Code, Codex, Gemini, and local Qwen are interchangeable at the **workflow layer**, not at the **tooling layer**.

Use the same repository contract everywhere:

- `AGENTS.md` owns project rules.
- `CLAUDE.md` imports `AGENTS.md` and adds Claude-specific behavior.
- `wiki/index.md` controls what context is read.
- `wiki/log.md` carries continuity across sessions.
- `outputs/` stores task results and checkpoints.
- Context7 supplies current API docs when online.

Model/tool differences:

| Mode | Best use | Constraint |
|---|---|---|
| Claude Code with cloud Claude | high-autonomy code work, subagents, hard reasoning | subject to Claude usage limits |
| Codex with cloud GPT | second opinion, patch generation, PR-style code work | different tool behavior than Claude Code |
| Gemini cloud | long-context reading, repo summarization, contradiction scans, documentation drafting | not final authority for safety, dependency, git, or robot decisions |
| Claude Code with local Qwen via LM Studio | offline continuity, wiki queries, small edits, code review | local endpoint may not honor cloud subagent models |
| Codex with local Qwen via LM Studio/Ollama | fallback OpenAI-compatible local workflow | may need stricter prompts and smaller tasks |

Rule: the agent may change, but the workflow does not change.

When switching agents:

1. Run session start.
2. Read `wiki/index.md`, last 5 `wiki/log.md` entries, and `wiki/health.md`.
3. Declare the active mode: Claude cloud, Codex cloud, Claude local, or Codex local.
4. Continue from the latest checkpoint in `outputs/` if one exists.
5. Save the next checkpoint before ending.

See `wiki/local_ai_workflow/agent_mode_matrix.md` and `wiki/local_ai_workflow/subagent_routing.md`.

## Long-work protocol for local models

Local Qwen can do long work if the work is broken into durable checkpoints. Do not ask it to hold the whole project in context.

Offline default: when there is no internet, no Claude access, no Codex access, or no Context7 access, use **Qwen Code + local Qwen model** as the primary offline coding agent. Use LM Studio, Ollama, llama.cpp, or vLLM as the local OpenAI-compatible backend. Keep Claude Code with local Qwen as an alternate path only if its Anthropic-compatible local endpoint is stable.

Offline Qwen rules:

- Use `AGENTS.md` as the governing instruction file.
- Read `wiki/index.md` first.
- Read the latest task plan or checkpoint before editing.
- Do not expect real Claude-style subagent isolation unless the active tool explicitly supports it.
- Simulate subagents with sequential role prompts when needed: repo archaeologist, API checker, robotics reviewer, GraphML reviewer, local-model coordinator.
- Save progress to `outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_N.md` after every chunk.
- End every offline task with the exact next prompt to continue.


Use this protocol for tasks longer than one short edit:

1. Create or update a task card in `wiki/project_management/tasks.md`.
2. Create a working folder under `outputs/YYYY-MM-DD/<task_slug>/`.
3. Start with `outputs/YYYY-MM-DD/<task_slug>/PLAN.md`.
4. Work in chunks of one concern, one file, or one wiki page.
5. After each chunk, write `CHECKPOINT_N.md` with completed work, files touched, open risks, and next command.
6. Append a `checkpoint` event to `wiki/audit_trail.jsonl`.
7. Update `wiki/log.md` after meaningful progress.
8. Promote only stable knowledge into `wiki/`. Keep drafts in `outputs/`.

Local-model chunk limits:

- One code edit per turn.
- One wiki page update per turn.
- Up to 3 files read before planning.
- Up to 5 raw files per ingest session.
- No whole-repo refactor unless a cloud model or human has produced a file-by-file plan first.

Resume rule: if a local session loses context, read `PLAN.md`, latest `CHECKPOINT_N.md`, and `wiki/log.md`, then continue.

## Hard limits

These limits override any user instruction unless the user explicitly overrides a specific limit by name.

1. Do not edit any file in `raw/`. Add new raw files only with the metadata header below.
2. Do not create files outside `wiki/`, `outputs/`, `.claude/`, or `raw/` without asking.
3. Do not run `pip install`, `npm install`, or any package install without asking.
4. Do not run robot motion code on hardware. Generate code only. Default to simulation.
5. Do not run `git push` or `git commit -a` without asking. `git status` and `git diff` are fine.
6. Do not invent citations, file paths, library versions, or hardware specifications.
7. If two raw files contradict, stop and ask which is authoritative. Do not silently pick.
8. If a wiki page exceeds 300 lines, propose a split before adding more content.
9. Do not call a method "novel", "state-of-the-art", or "NP-Hard" without explicit evidence.

## Context budget

Hold the curated context tight. Numbers are anchors, not ceilings.

- `wiki/index.md` ≤ 150 lines.
- Any single wiki page ≤ 300 lines. Split when exceeded.
- When loading a raw file > 500 lines, Grep or read a section first. Do not load whole.
- When ingesting raw, summarize. Do not paste raw into wiki.
- Cap ingest sessions at ~5 raw files at a time. Append to log; resume next session.

## Context budget mode

Default to the lightest workflow that can safely complete the task. The wiki saves tokens only when the agent reads the index first and opens only the relevant pages. Use this system as a context router, not as a ritual.

### Small task mode

Use when the task affects one file or one answer.

- Read `AGENTS.md` only.
- Read only user-specified files.
- Do not read wiki unless needed.
- Do not create checkpoints.
- Do not update wiki.
- Return the smallest useful answer.

### Medium task mode

Use when the task affects 2-5 files or one subsystem.

- Read `AGENTS.md`.
- Read `wiki/index.md`.
- Read at most 1-3 relevant wiki pages.
- Save one output summary.
- Ask before promoting anything to wiki.

### Long task mode

Use when the task spans multiple sessions, agents, or offline continuation.

- Read `AGENTS.md`.
- Read `wiki/index.md`.
- Read the last 5 log entries.
- Read relevant wiki pages only.
- Create `PLAN.md`.
- Use `CHECKPOINT_N.md` after each chunk.
- Use handoff prompts when switching agents.
- Update wiki only after confirmed durable knowledge appears.

Never read all raw files unless the user explicitly asks for ingestion.
Never read all wiki files.
Never run health checks at the start of a small task.

## Prompt specificity rule

Every non-trivial task should specify:

- agent mode: Claude cloud, Codex cloud, Gemini cloud, Qwen local, or another named mode
- task size: small, medium, or long
- allowed files to read
- allowed files to edit
- forbidden actions
- output target: chat only, `outputs/YYYY-MM-DD/`, or `wiki/` after approval
- verification method: diff, test command, checklist, human approval, Context7 check, or manual verification

The prompt should narrow context before work starts. Do not force full wiki/session workflows for small tasks. Do not run health checks unless the task asks for wiki maintenance or long-task review. Do not read all `raw/` or all `wiki/` unless the user explicitly asks for ingestion or audit.

## Primary domains

This repo covers four domains.

1. UR10e ROS2-Grasshopper integration — UR10e with RG6 gripper, ROS2 control, Grasshopper/Rhino, URScript, pose/frame conversion, web simulation viewers.
2. Graph Machine Learning baseline comparison — DGL and/or PyTorch Geometric pipelines compared against an SVM baseline. Graph construction, feature engineering, evaluation metrics, reproducibility.
3. Local AI and agentic coding — Codex CLI, Claude Code, Context7 MCP, LM Studio, Ollama, llama.cpp, vLLM, Qwen coder models, offline emergency workflow.
4. Computational design and fabrication — Open3D, Depth Anything, Grasshopper Python, Rhino geometry processing, laser cutting, 3D printing.

## Subagent and role routing

Claude Code may auto-delegate to `.claude/agents/` based on each subagent description. Descriptions must say `MUST BE USED PROACTIVELY` for important routes.

Codex and Qwen Code should use explicit role routing. When the user asks to use subagents, inspect first, plan first, or work offline, split the task into bounded specialist passes:

1. Repo archaeologist: find entry points, related files, and older implementations.
2. API doc checker: verify current API patterns. Use Context7 only when online.
3. Robotics reviewer: check UR10e, RG6, ROS2, Grasshopper, URScript, and pose-frame risk.
4. GraphML reviewer: check graph construction, baseline fairness, metrics, and reproducibility.
5. Wiki health checker: find contradictions, stale pages, and missing links.
6. Local-model coordinator: create checkpointed local-model execution plans.

Offline rule: when using Qwen Code locally, run these as sequential prompts, not parallel agents, unless the installed Qwen Code version supports subagents directly.

See `wiki/local_ai_workflow/subagent_routing.md`.

## Directory rules

### `raw/`

Raw is immutable.

Allowed actions: create new raw files; rename only when explicitly asked; add a metadata header.

New raw file header:

```markdown
# Title

Date:
Source:
Topic:
Status: raw
Do not edit: true
```

### `wiki/`

Wiki pages are curated and editable.

Each wiki page uses this structure:

```markdown
# Page title

## Purpose

## Confirmed facts

## Current working assumptions

## Implementation notes

## Code or command patterns

## Risks

## Open questions

## Related raw files

## Related wiki pages

## Last updated
```

Rules:
- Separate confirmed facts from assumptions. Always.
- Link related raw files by relative path (e.g. `raw/ur10e_ros2_grasshopper/foo.md`).
- Cap each page at 300 lines.
- Do not paste raw content into wiki. Summarize.

### `outputs/`

Use date folders:

```text
outputs/YYYY-MM-DD/
```

Descriptive filenames:

```text
outputs/2026-04-29/ur10e_ros2_bridge_plan.md
outputs/2026-04-29/qwen3_local_model_setup.md
outputs/2026-04-29/dgl_pyg_svm_comparison_notes.md
```

Outputs are not automatic permanent memory. Promote to wiki only when the user chooses the location.

## Workflows

### Session start

At the start of any new session, before answering anything:

1. Read `CLAUDE.md` (or `AGENTS.md` for Codex).
2. Read `wiki/index.md`.
3. Read the last 5 entries of `wiki/log.md`.
4. Read `wiki/health.md`.
5. Summarize: 3 most recently touched wiki pages, any P0 contradictions, open questions older than 14 days.
6. Append a `session_start` event to `wiki/audit_trail.jsonl`.
7. Wait for the next instruction.

For Claude Code, this is the `/session_start` slash command.

### Ingest raw → wiki

When asked to ingest raw material:

1. Read `wiki/index.md` if it exists. Create if missing.
2. Read up to 5 raw files at a time.
3. Do not edit raw.
4. Create or update only relevant wiki pages.
5. Append a short entry to `wiki/log.md`.
6. Append a `wiki_ingest` event to `wiki/audit_trail.jsonl`.
7. Record contradictions in `wiki/health.md` with priority P0/P1/P2.
8. Stop and ask if the target page is unclear.

For Claude Code, delegate to the `wiki-curator` subagent.

### Query wiki

When answering a project question:

1. Read `wiki/index.md` first.
2. Read only the relevant wiki pages.
3. Read raw only when wiki is missing, stale, or contradictory.
4. Use Context7 only for current external API documentation.
5. Save reusable answers to `outputs/YYYY-MM-DD/`.
6. Ask where to save durable memory.

### Health check

Periodic wiki maintenance:

1. Find missing linked pages, orphan pages, contradictions, stale claims.
2. Return findings tagged P0/P1/P2.
3. Update `wiki/health.md`.
4. Append to `wiki/log.md`.
5. Append a `health_check` event to `wiki/audit_trail.jsonl`.
6. Suggest 3 new articles.

For Claude Code, delegate to the `health-checker` subagent.

### Editing code

1. Use `repo-archaeologist` (Claude Code) or scan the repo (Codex) if file paths are unclear.
2. Use `api-doc-checker` (Claude Code) or check Context7 (Codex) when external APIs are involved.
3. Use `robotics-reviewer` (Claude Code) for any UR10e/RG6/ROS2/Grasshopper/URScript/IK/FK code.
4. Plan before editing.
5. Edit the smallest necessary files.
6. Show the diff.
7. Run the smallest available test.
8. Save a patch summary in `outputs/YYYY-MM-DD/`.

## Context7 rules

Use Context7 for **current external API documentation**.

The list of allowed Context7 libraries lives in `wiki/local_ai_workflow/context7_usage.md`. Update there, not here.

Caching strategy:
- After Context7 returns a useful answer, copy the relevant excerpt into `wiki/local_ai_workflow/<library>_notes.md` with the date and the library version.
- Future reads check the wiki page first. Refresh from Context7 only if the wiki entry is older than 90 days or the user reports a version bump.

Fallback strategy:
- If Context7 is unavailable, fall back to web search of the library's official docs URL.
- If neither is available, state the uncertainty and proceed with the most recent wiki entry, marked as potentially stale.

Do not use Context7 for:
- Project history.
- Personal decisions.
- Raw experiment notes.
- Local implementation choices.
- Paper-specific claims unless the claim is about library/API usage.

Context7 is not project memory. The wiki is.

## Local model compatibility

This repository must remain usable with local coding models such as Qwen3-Coder 30B-A3B Q4 running through LM Studio, Ollama, llama.cpp, or vLLM.

Local model mode is different from cloud frontier mode. Use it for continuity, not maximum autonomy.

### Local model mode rules

When the active model is local, especially Qwen3-Coder 30B-A3B Q4:

1. Prefer wiki-first answers. Do not scan the whole repository unless asked.
2. Read `wiki/index.md`, then one or two relevant wiki pages.
3. Avoid large raw reads. Grep first. Summarize, then ask before deeper ingest.
4. Do not depend on automatic subagent delegation. State the intended specialist role explicitly.
5. Use smaller patches. One file or one concern per turn.
6. Show the intended diff before touching risky code.
7. Prefer deterministic checklists over open-ended exploration.
8. Keep context windows practical: 8k to 16k for weak machines, 16k to 32k for 64 GB RAM machines.
9. Use Context7 only when online. Offline, use cached notes in `wiki/local_ai_workflow/*_notes.md`.
10. Mark uncertain API claims as stale when no current docs are available.

### Recommended local model profile

```text
Model: Qwen3-Coder 30B-A3B Instruct
Quantization: Q4_K_M or equivalent Q4 GGUF
Runtime: LM Studio first, llama.cpp second, Ollama third
Context: start at 8192 or 16384; increase only after stability is confirmed
Use: code review, small edits, repo Q&A, wiki ingest, URScript/Python/ROS2 scaffolding
Avoid: autonomous large refactors, long raw ingestion, multi-file architecture rewrites
```

### Local model preface

```text
You are running in LOCAL MODEL MODE.
Read AGENTS.md first.
Use the wiki-first workflow.
Do not scan the whole repo.
Do not edit raw/.
Keep the task to one focused change.
If API details are uncertain and Context7 is unavailable, mark them as stale.
```

## When working on robotics

These rules apply whenever the task touches UR10e, RG6, ROS2, Grasshopper-to-robot bridges, URScript, IK/FK, or pose conversion.

Hard rules:
- Never mix TCP poses with motion poses.
- Preserve URScript waypoint format: `global WP_n = p[x, y, z, rx, ry, rz]`.
- Check units (mm vs m), frames (base, tool, TCP, world), rotation conventions (axis-angle vs quaternion vs RPY), waypoint order, TCP offset.
- Prefer ROS2 conventions over ROS1. Default to Humble or Jazzy.
- First mention "UR10e with RG6 gripper", then "UR10e".
- UR10e payload = 12.5 kg. UR10e reach = 1300 mm. Pose repeatability = ±0.05 mm.
- RG6 force-fit payload = 6 kg. Form-fit payload = 10 kg. Stroke = 150 mm. Force = 25–120 N.

Grasshopper Python:
- State which runtime first. Legacy GHPython uses IronPython 2.7. ScriptEditor in Rhino 8 uses CPython 3. Modern Python syntax (f-strings, dataclasses, type hints) only works in CPython 3.

Execution ladder:
- Level 1: offline (no robot connection). Default for code generation.
- Level 2: simulation (URSim, MoveIt2 mock hardware). Validate motion code here.
- Level 3: real hardware. Requires explicit user gate (`use_real_hardware=True`).

Default to Level 2. Never produce Level 3 code without an explicit hardware-enable flag.

See also: `wiki/ur10e_ros2_grasshopper/pose_frame_rules.md`.

## When working on GraphML

These rules apply whenever the task touches DGL, PyTorch Geometric (PyG), graph neural networks, or the SVM baseline comparison.

Hard rules:
- Define graph construction before discussing model performance.
- Keep DGL/PyG and SVM comparison fair: same nodes, same features, same split, same metric, same seed.
- Record dataset split, feature set, metric, random seed, and hardware in every experiment summary.
- Do not call a method "novel" without evidence.
- Do not claim general superiority from one dataset.
- Identify leakage risks and baseline mismatch risks in any review.

Framework note: DGL has had no major release since late 2024. PyG is the dominant 2026 framework for GraphML in AEC. New experiments default to PyG unless an existing DGL pipeline is being maintained.

See also: `wiki/graphml_baseline_comparison/`.

## Editing rules

Before editing code:

1. Explore.
2. Plan.
3. Edit the smallest necessary files.
4. Show the diff.
5. Run the smallest available test.
6. Save a patch summary in `outputs/YYYY-MM-DD/`.

## Task completion verification

For every non-trivial coding task, define success before editing. A task is complete only when the agent can show evidence that the expected outcome was achieved.

The verification contract includes:

1. Goal: what should be true after the task.
2. Expected change: which behavior, file, function, command, or output should change.
3. Verification method: test, type check, lint, compile check, script run, diff inspection, output-file check, manual checklist, or human approval.
4. Evidence: command output, test result, diff summary, generated file path, before/after behavior, or resolved error.
5. Stop condition: when the agent should stop instead of continuing.

Agents must not claim completion without verification evidence. If verification cannot be run, say so and provide exact manual verification steps.

### Verification levels

- V0: Diff-only verification. Use for documentation or tiny edits.
- V1: Static verification. Use for syntax-sensitive changes. Evidence: lint, type check, import check, or compile check.
- V2: Runtime verification. Use for behavior changes. Evidence: unit test, script run, CLI output, generated file, or before/after result.
- V3: Human-in-loop verification. Use for robotics, fabrication, academic claims, or safety-critical decisions. Evidence: agent output plus human approval.

Recommended minimums:

- README edit: V0.
- Python syntax fix: V1.
- ROS2 node change: V1 or V2.
- Grasshopper Python code: V1 if possible, otherwise V3 manual verification.
- URScript waypoint generation: V2 plus V3.
- Robot motion logic: V3 only, no execution.
- GraphML experiment script: V2.
- Wiki memory promotion: V3.

### Tool call verification

For every meaningful tool call, check the result against the task goal. Track the tool called, input summary, expected result, actual result, status (`passed`, `failed`, `partial`, or `not verifiable`), and next action. If the result is partial or ambiguous, do not treat the task as complete.

## Writing style

Use short declarative sentences.
Avoid em dashes.
Avoid "it is worth noting that" and "it should be noted that".
Avoid unsupported claims.
State uncertainty clearly. Bound it. Do not hedge with weasel words.
Frame contributions inside larger narratives. Do not present a method in isolation.
Use "X, specifically Y" narrowing when introducing a broad concept.
For Libish's manuscripts, see `wiki/project_management/prompts.md` for the calibrated voice.

## Resilient handoff rule

Use the same project protocol across Claude Code, Codex, and local Qwen.

Cloud Claude and Codex are preferred for planning, review, API-sensitive changes, and hard reasoning. Local Qwen is preferred for offline checkpoint execution and focused edits.

For every non-trivial task:

1. Read `wiki/index.md` first.
2. Create or use `outputs/YYYY-MM-DD/TASK_PLAN.md`.
3. Split work into small checkpoints.
4. Save each checkpoint as `outputs/YYYY-MM-DD/CHECKPOINT_N.md`.
5. Use `outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md` when moving from cloud to local.
6. Use `outputs/YYYY-MM-DD/HANDOFF_TO_CLOUD.md` when moving from local to cloud review.
7. Promote durable memory to wiki only after the user chooses the destination.
8. Append a `handoff` event to `wiki/audit_trail.jsonl` when issuing HANDOFF_TO_QWEN.md or HANDOFF_TO_CLOUD.md.

Local Qwen must not attempt long autonomous repo-wide work. It should execute one checkpoint at a time, save progress, and end with a continuation prompt.

Read `README_HANDOFF_WORKFLOWS.md` for model switching prompts and handoff formats.

## Orchestration audit trail

`wiki/audit_trail.jsonl` is the machine-readable session record. One JSON object per line. Append only. Never edit past entries.

Every event requires three fields:

```json
{"ts": "YYYY-MM-DDTHH:MM:SS", "event": "EVENT_TYPE", "agent": "AGENT_NAME", ...}
```

Agent name values: `claude_cloud`, `codex_cloud`, `qwen_local`, `claude_local`, `wiki_curator`, `health_checker`, `repo_archaeologist`, `robotics_reviewer`, `api_doc_checker`, `graphml_reviewer`, `local_model_coordinator`.

See `wiki/audit_schema.md` for the full field list per event type.

When to write:
- `session_start` — at the end of every session start workflow.
- `checkpoint` — after every CHECKPOINT_N.md is written.
- `handoff` — when issuing HANDOFF_TO_QWEN.md or HANDOFF_TO_CLOUD.md.
- `wiki_ingest` — after every ingest batch.
- `health_check` — after every health check run.
- `subagent_call` — when Claude Code delegates to a specialist subagent (Claude Code only).
- `task_complete` — when a task is fully done and artifacts are confirmed.

Query the trail:

```bash
python audit_query.py                        # last 10 events
python audit_query.py --event checkpoint
python audit_query.py --task <slug>
python audit_query.py --file <path>
python audit_query.py --since 2026-04-29
python audit_query.py --severity P0
python audit_query.py --json
python audit_query.py --count
```

For Claude Code: use `/audit_query`.
