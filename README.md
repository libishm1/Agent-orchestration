# Agent Orchestration: Resilient AI Context Workflow

A working prototype for managing project context across Claude Code, Codex, and local models such as Qwen.

This repository provides a curated project-memory scaffold for engineering workflows that need continuity across sessions, tools, and compute modes. It replaces blind RAG-style context loading with a structured `raw/ → wiki/ → outputs/` system.

The goal is simple:

> Keep project memory stable while switching between cloud agents and offline local models.

## Status

Experimental but usable workflow scaffold.

This is not a production orchestration framework. It is a structured method for making AI coding workflows more reliable across Claude Code, Codex, and local Qwen sessions.

## Core Idea

Most AI coding failures come from context drift.

An agent reads too much.
Another agent reads too little.
A local model forgets the plan.
Cloud limits expire.
A repo has old scripts, duplicated files, and hidden assumptions.

This template solves that with three memory layers:

```text
raw/      = immutable evidence
wiki/     = curated project memory
outputs/  = generated answers, checkpoints, handoffs, and artifacts
```

Agent rules live in:

```text
AGENTS.md   = shared rules for Codex, Claude Code, Qwen Code, and other agents
CLAUDE.md   = thin Claude Code wrapper that imports AGENTS.md
GEMINI.md   = thin Gemini wrapper that points to AGENTS.md
```

External API compliance is handled through Context7 where available.

## What This Is

This is a context-management and handoff system for:

* Claude Code
* Codex
* Qwen Code
* local Qwen models through LM Studio, Ollama, llama.cpp, or compatible servers
* Context7-assisted API documentation checks
* multi-session coding workflows
* online/offline engineering work

It is designed for robotics, Graph Machine Learning, computational design, and local AI workflows.

## What This Is Not

* Not a vector database.
* Not an autonomous agent framework.
* Not token-efficient by default.
* Not a guarantee that local models match Claude or Codex.
* Not a replacement for tests, Git history, or code review.
* Not safe for robot execution without human validation.
* Not a system for running physical robot motion commands automatically.

## How This Compares To Agent Frameworks

This repo is not a full orchestrator. It does not schedule agents, manage state graphs, run sandboxed autonomous tasks, or replace coding agents.

Use LangGraph, CrewAI, AutoGen, or similar frameworks when you need programmable multi-agent execution. Use Cline, Roo Code, Continue, Qwen Code, Claude Code, Codex, or Gemini when you need actual coding-agent execution.

Use this repo when you need the layer between those tools: shared project memory, human verification, explicit context routing, task verification, and online/offline handoff continuity.

Intended stack:

```text
Claude Code = deep planning and review
Codex = cloud patch worker
Gemini = long-context scout and summarizer
Qwen Code = offline local execution
Roo/Cline/Continue = optional VS Code local-model execution
This repo = memory, prompts, handoffs, checkpoints, and verification contracts
```

## Human Verification

Agents may propose, draft, inspect, summarize, patch, and verify. Humans approve task scope, files to edit, dependency installation, robot motion logic, physical fabrication decisions, durable wiki memory, git commits or pushes, and academic claims.

No agent output becomes project truth until it is verified and promoted into `wiki/`. Human verification should reduce scope, not add ceremony. For small tasks, one compact approval instruction is enough. For medium, long, or high-risk tasks, use the short checklist in `wiki/project_management/human_verification_checklist.md`.

## Task Completion Verification

For every non-trivial coding task, define success before editing. A task is complete only when there is evidence that the expected outcome was achieved.

Verification levels:

```text
V0 = diff-only verification for documentation or tiny edits
V1 = static verification such as compile, lint, type, import, or syntax check
V2 = runtime verification such as tests, script output, CLI output, or generated files
V3 = human-in-loop verification for robotics, fabrication, academic claims, or safety decisions
```

If verification cannot be run, the agent must say so and provide exact manual verification steps.

## Why This Exists

Cloud models are strong, but limits expire.

Local models are available offline, but they struggle with long context and open-ended repo work.

This template creates a shared workflow so that:

```text
Claude Code can plan.
Codex can patch.
Gemini can summarize long context.
Qwen can continue offline.
Cloud models can review later.
The wiki keeps stable memory.
Outputs preserve handoffs and checkpoints.
```

The system is useful when working across:

* travel
* power outages
* internet outages
* Claude or Codex usage limits
* large repositories
* long-running research projects
* robotics workflows where frame, unit, and pose mistakes matter

## Project Structure

The repo root includes `README.md`, `GEMINI.md`, and the project scaffold folder:

```text
project_context_template/
├── AGENTS.md
├── CLAUDE.md
├── HOW_TO_USE.md
├── README_HANDOFF_WORKFLOWS.md
├── CONTEXT7_SETUP.md
├── LOCAL_MODEL_SETUP.md
├── SETUP_PROMPTS.md
├── audit_query.py
│
├── .claude/
│   ├── agents/
│   ├── commands/
│   └── settings.json
│
├── raw/
│   ├── 00_inbox/
│   ├── ur10e_ros2_grasshopper/
│   ├── graphml_baseline_comparison/
│   ├── local_ai_codex_claude/
│   ├── fabrication_workflows/
│   └── references/
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── health.md
│   ├── audit_trail.jsonl
│   ├── audit_schema.md
│   ├── glossary.md
│   ├── ur10e_ros2_grasshopper/
│   ├── graphml_baseline_comparison/
│   ├── local_ai_workflow/
│   └── project_management/
│
└── outputs/
    └── YYYY-MM-DD/
```

## Memory Layers

### raw/

`raw/` stores immutable evidence.

Use it for:

* meeting notes
* copied conversations
* screenshots converted to notes
* code snippets
* paper notes
* setup notes
* URLs
* experiment logs
* hardware observations

Rules:

* Do not edit existing raw files.
* Do not delete raw files.
* Do not treat raw as final truth.
* Resolve contradictions in `wiki/`, not in `raw/`.

### wiki/

`wiki/` stores curated project memory.

Use it for:

* stable implementation notes
* decisions
* assumptions
* known risks
* API notes
* experiment design
* robotics rules
* GraphML comparison notes
* local model workflow notes

Rules:

* Read `wiki/index.md` first.
* Open only relevant pages.
* Keep pages concise.
* Split pages when they grow too large.
* Record uncertainty explicitly.
* Link back to raw evidence when possible.

### outputs/

`outputs/` stores generated work.

Use it for:

* task plans
* checkpoint files
* handoff notes
* patch summaries
* code reviews
* experiment summaries
* generated reports
* answers worth saving temporarily

Rules:

* Outputs are not permanent memory by default.
* Promote useful outputs to `wiki/` only when confirmed.
* Use date folders: `outputs/YYYY-MM-DD/`

## Supported Workflows

### Claude Code

Best for:

* complex reasoning
* architecture decisions
* repo-wide planning
* high-risk robotics code review
* subagent workflows
* cloud-assisted debugging

Claude Code uses:

```text
CLAUDE.md
.claude/agents/
.claude/commands/
.claude/settings.json
```

Claude Code can use specialist subagents for focused tasks.

### Codex

Best for:

* patch-oriented coding
* second opinions
* PR-style changes
* code review
* test-driven fixes

Codex uses:

```text
AGENTS.md
SETUP_PROMPTS.md
```

Codex routing in this template is prompt-driven. Use explicit prompts when you want subagent-style decomposition.

### Gemini

Best for:

* long-context inspection
* repo summarization
* wiki draft generation
* contradiction scanning
* handoff compression

Gemini uses:

```text
GEMINI.md
project_context_template/AGENTS.md
```

Gemini should summarize and propose. It is not final authority for robot safety, dependency installation, git push, destructive commands, or academic claims.

### Local Qwen

Best for:

* offline travel work
* emergency coding
* focused edits
* selected-file review
* checkpointed continuation
* local repo notes
* small to medium patches

Local Qwen should not be treated like a cloud Claude replacement.

Use it as:

```text
offline checkpoint execution worker
```

Recommended local workflow:

```text
PLAN.md → CHECKPOINT_001.md → CHECKPOINT_002.md → HANDOFF_TO_CLOUD.md
```

### Context7

Context7 is used for current external API documentation.

Use it for:

* ROS2
* rclpy
* ros2_control
* MoveIt2
* FastAPI
* Flask
* WebSocket APIs
* React
* Three.js
* Open3D
* DGL
* PyTorch Geometric
* scikit-learn
* vLLM
* llama.cpp
* LM Studio
* Claude Code
* Codex

Do not use Context7 as project memory. Project memory lives in `wiki/`.

## Context Budget Modes

This system is not token-efficient by default.

It becomes token-efficient only when used as a context router.

Use the lightest workflow that can safely complete the task.

### Small Task Mode

Use for one-file edits, quick bug fixes, small explanations, single function review.

```text
Read AGENTS.md.
Read only the target file.
Do not read the whole wiki.
Do not update wiki.
Do not create checkpoints.
Do not run health checks.
```

### Medium Task Mode

Use for one subsystem, 2 to 5 files, one wiki article update.

```text
Read AGENTS.md.
Read wiki/index.md.
Read at most 1 to 3 relevant wiki pages.
Save one summary to outputs/YYYY-MM-DD/.
Ask before promoting memory to wiki.
```

### Long Task Mode

Use for multi-session work, cloud to local handoff, large research workflows.

```text
Read AGENTS.md.
Read wiki/index.md.
Read last 5 entries of wiki/log.md.
Read relevant wiki pages only.
Create PLAN.md.
Use CHECKPOINT_N.md after each chunk.
Create handoff notes when switching agents.
Update wiki only after durable knowledge is confirmed.
```

## Agent Mode Matrix

| Mode | Best Agent | Use Case | Memory Strategy |
|---|---|---|---|
| High-level planning | Claude Code cloud | architecture, reasoning, risky decisions | wiki + selected outputs |
| Patch implementation | Codex cloud | code changes, PR-style tasks | AGENTS.md + target files |
| Long-context scouting | Gemini cloud | large-file reading, summarization, contradiction scans | selected files + wiki |
| Offline execution | Qwen Code local | travel, outages, focused edits | PLAN + checkpoints |
| API compliance | Context7-assisted agent | current docs | Context7 + wiki notes |
| Review | Claude or Codex cloud | verify Qwen output | checkpoints + diff |
| Durable memory | any agent | save stable knowledge | promote outputs to wiki |

## Quick Start

### 1. Clone

```bash
git clone https://github.com/libishm1/Agent-orchestration.git
cd Agent-orchestration/project_context_template
```

### 2. Open in VS Code

```bash
code .
```

### 3. Start a Claude Code session

```text
/session_start
```

This reads `CLAUDE.md`, `wiki/index.md`, last 5 entries of `wiki/log.md`, and `wiki/health.md`.

### 4. Start a Codex session

Use the session-start prompt from `SETUP_PROMPTS.md`.

### 5. Start a local Qwen session

```text
Read AGENTS.md.
Read wiki/index.md.
Use local model mode.
Do not inspect the whole repo.
Ask for exact files if needed.
```

## Daily Workflow

### Start

```text
/session_start
```

### Add Evidence

Drop new material into `raw/<topic>/`.

### Ingest Raw Into Wiki

```text
/ingest_raw
```

### Ask a Project Question

```text
/query_wiki <question>
```

### Save Memory

```text
/save_memory <wiki-path>
```

### Health Check

```text
/health_check_wiki
```

Use weekly or after large ingest operations. Do not run for small tasks.

## Orchestration Audit Trail

`wiki/audit_trail.jsonl` is the machine-readable session record.

Every agent action is recorded as one JSON line:

```json
{"ts": "2026-04-29T14:40:00", "event": "checkpoint", "agent": "codex_cloud", "task": "grasshopper_websocket_pose_pipeline", "outcome": "passed"}
```

Query it:

```bash
python audit_query.py                          # last 10 events
python audit_query.py --event checkpoint
python audit_query.py --task <slug>
python audit_query.py --file <path>
python audit_query.py --since 2026-04-29
python audit_query.py --severity P0
python audit_query.py --json
python audit_query.py --count
```

Or use `/audit_query` in Claude Code.

See `wiki/audit_schema.md` for the full event schema.

## Handoff Workflows

### Cloud to Qwen

Use before travel, outages, or Claude/Codex limit exhaustion.

```text
Read AGENTS.md.
Prepare a handoff for local Qwen.

Create:
outputs/YYYY-MM-DD/PLAN.md
outputs/YYYY-MM-DD/NEXT_PROMPT_FOR_QWEN.md

The handoff must include:
1. task goal
2. exact files to read
3. files not to touch
4. current assumptions
5. known risks
6. checkpoint sequence
7. smallest test command
8. stop condition
```

### Qwen Offline Checkpoint

```text
Read AGENTS.md.
Read wiki/index.md.
Read outputs/YYYY-MM-DD/PLAN.md.
Read the latest CHECKPOINT file if it exists.

Complete only the next checkpoint.
Read only the listed files.
Save progress to outputs/YYYY-MM-DD/CHECKPOINT_N.md.
End with the exact next prompt to continue.
```

### Qwen to Cloud Review

```text
Read AGENTS.md.
Review Qwen offline work.

Read:
outputs/YYYY-MM-DD/PLAN.md
outputs/YYYY-MM-DD/CHECKPOINT_*.md
git diff

Check:
1. whether the task goal was met
2. whether any files were touched unnecessarily
3. whether robotics, API, or GraphML constraints were violated
4. whether tests are missing
5. what should be promoted to wiki
```

See `README_HANDOFF_WORKFLOWS.md` for all handoff prompts.

## Specialist Claude Subagents

Claude Code can use custom subagents from `.claude/agents/`.

| Subagent | Purpose | Model |
|---|---|---|
| `wiki-curator` | ingest raw into wiki | haiku |
| `health-checker` | find stale pages, contradictions, orphan pages | haiku |
| `repo-archaeologist` | inspect old repos and identify relevant files | sonnet |
| `robotics-reviewer` | review UR10e, RG6, ROS2, Grasshopper, URScript risks | sonnet |
| `api-doc-checker` | check current API usage with Context7 | sonnet |
| `graphml-reviewer` | review DGL, PyG, SVM comparison logic | sonnet |
| `local-model-coordinator` | break work into Qwen-safe checkpoints | haiku |

## Domain Coverage

### UR10e ROS2-Grasshopper Integration

The wiki covers:

* UR10e with RG6 gripper
* ROS2 bridge patterns
* Grasshopper and Rhino workflows
* URScript generation
* pose and frame rules
* TCP pose versus motion pose separation
* IK/FK and waypoint review
* simulation and web viewer notes

Non-negotiable rule:

```text
Never mix TCP poses with motion poses.
```

Grasshopper Python rule:

```text
Always state the runtime first:
- Legacy GHPython component: IronPython 2.7, no f-strings, no dataclasses
- Rhino 8 ScriptEditor Python 3: CPython, modern syntax allowed
```

### Graph Machine Learning Baseline Comparison

The wiki covers graph construction, dataset splits, DGL pipeline, PyTorch Geometric pipeline, SVM baseline, feature engineering, metrics, comparison matrix, and reproducibility.

Rules:

```text
Define graph construction before discussing model performance.
Keep DGL, PyG, and SVM comparison fair: same nodes, features, split, seed, metric.
Record dataset split, feature set, metric, seed, and hardware in every summary.
Do not claim general superiority from one dataset.
```

### Local AI Workflow

The wiki covers Claude Code setup, Codex setup, Context7 usage, Qwen Code offline mode, LM Studio, Ollama, llama.cpp, vLLM experiments, local model constraints, and agent handoff rules.

## Local Model Expectations

Local models are useful, but they are not cloud Claude.

```text
Claude / Codex cloud = planner, reviewer, hard reasoning
Qwen local = focused offline execution worker
wiki = durable memory
outputs = task continuity
```

For local Qwen, prefer focused files, short checkpoints, explicit next prompts, small diffs, and low context.

Avoid whole-repo inspection, giant context windows, large autonomous refactors, raw-folder ingestion in one pass, and robot motion execution.

## Hard Limits

Agents must follow these limits:

* Do not edit `raw/`.
* Do not delete raw evidence.
* Do not run robot motion commands.
* Do not `git push` unless explicitly asked.
* Do not install packages without asking.
* Do not create files outside approved folders unless needed for the task.
* Do not run broad destructive shell commands.
* Do not claim robot safety without human validation.
* If raw files contradict each other, stop and ask which source is authoritative.

## Token Efficiency Warning

This system saves tokens only when agents:

```text
read wiki/index.md first
open only relevant pages
avoid reading all raw files
write compact checkpoints
promote only durable memory
```

Worst use: every agent reads AGENTS.md, all wiki pages, all raw files, all outputs, and all checkpoints every time.

Best use: agent reads AGENTS.md, wiki/index.md, and 1 to 3 relevant pages.

## Roadmap

Short-term:

* Add worked examples (cloud-to-Qwen handoff, pose-frame review, wiki ingest).
* Add a token-budget checklist.
* Add a sample UR10e pose-frame review.
* Add a sample GraphML baseline comparison plan.

Medium-term:

* Add validation scripts for folder structure.
* Add `wiki/health.md` checker improvements.
* Add examples for Codex and Qwen Code.

Long-term:

* Add optional GitHub issue templates.
* Add optional CI checks for forbidden raw edits.

## Permissions and Safety

* Read: any file.
* Write/Edit: `wiki/`, `outputs/`, `.claude/` only.
* `raw/` is append-only. No deletions.
* Bash is restricted to git, ls, pytest. Anything else requires explicit user approval.

## License

This project is maintained by Libish Murugesan at Alfaisal University.

Recommended license for reuse: MIT or Apache-2.0. Check individual subdirectories for specific licenses on robotics, ML, and local AI components.

## Support

* Questions: check `wiki/index.md` first.
* Setup help: see `HOW_TO_USE.md`.
* Issues: file in GitHub or add to `wiki/health.md`.
* Context lost: check `wiki/log.md` and `wiki/audit_trail.jsonl` for session history.

---

Last updated: 2026-04-30
Repository: https://github.com/libishm1/Agent-orchestration
Status: Experimental workflow scaffold
