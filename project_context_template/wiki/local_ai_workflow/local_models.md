# Local Models

## Purpose

Which local LLMs are evaluated for this project, on which runtime, and for which task. This page makes the template usable when the main agent is a local model such as Qwen3-Coder 30B-A3B Q4.

## Confirmed facts

- Three daily runtimes are supported: **LM Studio**, **Ollama**, and **llama.cpp**.
- A fourth runtime, **vLLM**, is reserved for Linux/server experiments with stronger GPUs.
- LM Studio is the default Windows route because it exposes both OpenAI-compatible and Anthropic-compatible local endpoints.
- Codex expects an OpenAI-compatible endpoint.
- Claude Code works best with an Anthropic-compatible endpoint.
- Default serious offline model: **Qwen3-Coder 30B-A3B Instruct Q4 GGUF**.
- Default fast fallback model: **Qwen2.5-Coder 7B Instruct Q5_K_M** or **Qwen3-Coder 8B Q5**.

## Current working assumptions

- Local models are an **offline continuity layer**, not a full replacement for Claude Sonnet, Opus, or GPT frontier models.
- Qwen3-Coder 30B-A3B Q4 is strong enough for serious code review, smaller edits, URScript/Python scaffolding, wiki work, and repo Q&A.
- It should not be trusted for large autonomous refactors without a human reviewing the diff.
- 64 GB system RAM + 8 GB VRAM is enough to run Qwen3-Coder 30B-A3B Q4 practically, but not cloud-fast.
- 2 TB internal NVMe storage is preferred over an external SSD for model files.
- Context windows above 32k may become slow or unstable on mid-tier laptops. Start with 8k or 16k.

## Recommended model ladder

| Tier | Model | Quant | Purpose | Notes |
|---|---|---:|---|---|
| Fast offline | Qwen2.5-Coder 7B Instruct | Q5_K_M | quick edits, small scripts | works on modest laptops |
| Balanced offline | Qwen2.5-Coder 14B Instruct | Q4_K_M/Q5_K_M | better reasoning, still manageable | good if 30B is too slow |
| Serious offline | Qwen3-Coder 30B-A3B Instruct | Q4_K_M | main local coding model | recommended target |
| Server/cloud | Qwen3-Coder larger variants, DeepSeek/Kimi/GLM coding models | varies | frontier-ish open model testing | not for this laptop |

## Runtime selection

### LM Studio

Use for Windows, VS Code, Claude Code, and quick local testing.

Strengths:
- GUI model download and loading.
- Local server on `http://localhost:1234`.
- OpenAI-compatible API for Codex-like clients.
- Anthropic-compatible `/v1/messages` API for Claude Code-like clients.

### Ollama

Use for CLI-first workflows and Codex OSS/local provider workflows.

Strengths:
- Simple pull/run flow.
- Good terminal workflow.
- Easy model switching.

Limitations:
- Model availability depends on Ollama registry or custom Modelfiles.
- Anthropic-compatible behavior may require a proxy depending on the client.

### llama.cpp

Use when you need maximum control.

Strengths:
- Direct GGUF execution.
- Fine control over context, GPU layers, batch size, KV cache, and server flags.

Limitations:
- More setup friction.
- API compatibility depends on the server build and flags.

### vLLM

Use after Linux/WSL/server setup is stable.

Strengths:
- Strong throughput serving.
- Good for multi-user or batched inference.

Limitations:
- Not the first route for an 8 GB VRAM laptop.
- More dependency weight.
- Better with safetensors than GGUF.

## Code or command patterns

### LM Studio server

In LM Studio:

```text
1. Download Qwen3-Coder 30B-A3B Instruct GGUF Q4.
2. Load the model.
3. Set context to 8192 or 16384 first.
4. Start Local Server.
5. Confirm server URL: http://localhost:1234
```

### Claude Code with LM Studio

PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:1234"
$env:ANTHROPIC_AUTH_TOKEN = "lmstudio"
claude
```

Bash:

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
claude
```

### Codex with LM Studio

Codex uses `~/.codex/config.toml`. A local profile can point at LM Studio's OpenAI-compatible endpoint.

```toml
[model_providers.lmstudio]
name = "LM Studio"
base_url = "http://localhost:1234/v1"
wire_api = "chat"
requires_openai_auth = false

[profiles.qwen3-local]
model_provider = "lmstudio"
model = "qwen3-coder-30b-a3b-instruct"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Run:

```bash
codex --profile qwen3-local
```

If the local server does not support a Codex-required endpoint, use LM Studio through its OpenAI-compatible chat endpoint or switch to Ollama/OSS mode.

### Codex with Ollama OSS mode

```bash
ollama list
codex --oss
```

Use this only after the target model is already pulled and tested.

### llama.cpp server example

```bash
./llama-server \
  -m models/Qwen3-Coder-30B-A3B-Instruct-Q4_K_M.gguf \
  -c 16384 \
  -ngl 99 \
  --host 127.0.0.1 \
  --port 8080
```

Then point compatible clients at the server URL. Confirm whether the build exposes OpenAI-compatible, Anthropic-compatible, or both endpoint families.

## Local model operating rules

When using Qwen3-Coder 30B-A3B Q4:

1. Use `wiki/index.md` first.
2. Read only relevant wiki pages.
3. Do not ingest more than 5 raw files per session.
4. Do not ask the model to "fix the repo". Ask for one file or one concern.
5. Do not trust tool-use blindly. Inspect diffs manually.
6. Prefer exact commands and checklists.
7. Keep code changes small.
8. Save patch summaries to `outputs/YYYY-MM-DD/`.
9. Promote durable memory into `wiki/` only after human review.

## Smoke test prompt

Use this after connecting a local model:

```text
You are running in LOCAL MODEL MODE.
Read AGENTS.md.
Read wiki/index.md.
Do not scan raw/.
Summarize the wiki structure in 10 bullets.
Then identify which two pages are relevant for a UR10e ROS2-Grasshopper question.
Do not edit files.
```

Expected behavior:
- reads the rule file
- reads index only
- does not scan raw
- gives a short answer
- does not invent missing wiki pages

## Risks

- **Quantization quality drop.** Q3 and below can damage coding reliability. Use Q4_K_M minimum.
- **Context length degradation.** A model may advertise long context but reason poorly at long ranges. Test 8k, 16k, 32k.
- **Tool-use support is uneven.** Local models may fail structured tool calls. Use manual prompts when needed.
- **VRAM exhaustion.** 30B Q4 on 8 GB VRAM will spill to RAM. Expect slower output.
- **Endpoint mismatch.** Codex, Claude Code, LM Studio, Ollama, and llama.cpp may expose different API shapes. Test each client separately.

## Open questions

- Which exact Qwen3-Coder 30B-A3B Q4 GGUF build is the most stable on the ThinkPad P53 after the 64 GB RAM and 2 TB SSD upgrade?
- Should the project maintain a `models/README.md` outside the repo with local model checksums and tested settings?
- Is LM Studio or Ollama more reliable for Codex on Windows in this specific setup?

## Related raw files

(populate via `/ingest_raw`)

## Related wiki pages

- [Overview](overview.md)
- [Offline workflow](offline_workflow.md)
- [Context7 usage](context7_usage.md)
- [Claude Code setup](claude_code_setup.md)
- [Codex setup](codex_setup.md)

## Last updated

2026-04-29


## Long-work strategy for local Qwen

Local Qwen should not be treated as weak. It should be treated as context-sensitive. It can complete long work when the long work is stored as external state.

Use files as memory:

- `wiki/index.md` tells the model where to look.
- `wiki/log.md` tells the model what happened recently.
- `outputs/YYYY-MM-DD/<task_slug>/PLAN.md` stores the task plan.
- `outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_N.md` stores progress.
- `wiki/project_management/tasks.md` stores durable task status.

Good local long-work tasks:

- ingest 3 to 5 raw notes into one wiki page
- review one ROS2 node
- rewrite one Grasshopper Python script
- generate one URScript helper
- compare one DGL/PyG/SVM experiment table
- update one setup page after a successful command test

Bad local long-work tasks:

- inspect the entire repo and fix everything
- ingest all raw folders in one pass
- refactor ROS2, Grasshopper, and web code in one prompt
- depend on fresh API details while offline

Recommended local prompt:

```text
You are running in LOCAL MODEL MODE with Qwen3-Coder 30B-A3B Q4.
Read AGENTS.md and wiki/index.md.
Read only the pages needed for this task.
Create or update outputs/YYYY-MM-DD/<task_slug>/PLAN.md.
Do one chunk only.
Write CHECKPOINT_N.md with the next command.
Do not edit raw.
Do not scan the whole repo.
```

## Interchangeability with Claude and Codex

Claude Code, Codex, and local Qwen should produce compatible project state because they all follow `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, and `outputs/` checkpoints.

They are not identical at the tool layer. Claude Code has subagents and slash commands. Codex uses `AGENTS.md` and prompt workflows. Local Qwen may not follow tool schemas as reliably as cloud models.

The safe interchange pattern is:

1. Cloud Claude or Codex creates a plan when the task is complex.
2. Local Qwen executes one chunk offline.
3. Local Qwen writes a checkpoint.
4. Cloud Claude or Codex reviews the diff later.
5. Stable knowledge is promoted to wiki.

This keeps long work possible without pretending that local Qwen has frontier-level context management.


## Qwen Code offline path

When fully offline, prefer Qwen Code with a local Qwen model for coding-agent work. Qwen Code can be pointed at OpenAI-compatible local endpoints through `~/.qwen/settings.json`. Use `wiki/local_ai_workflow/qwen_code_offline.md` for the exact workflow.

Recommended local hierarchy:

1. Qwen Code + local Qwen backend for offline coding-agent work.
2. Claude Code + LM Studio Anthropic-compatible endpoint as an alternate path.
3. LM Studio chat as the manual fallback.

Do not expect offline Qwen to perform long cloud-style autonomous work without checkpoints.
