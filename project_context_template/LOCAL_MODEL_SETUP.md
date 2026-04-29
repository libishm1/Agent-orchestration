# Local Model Setup

This template supports cloud agents and local models. The recommended serious offline model is **Qwen3-Coder 30B-A3B Instruct Q4 GGUF**.

## Target machine

Recommended minimum for the 30B Q4 workflow:

- 64 GB system RAM
- 2 TB internal NVMe SSD
- NVIDIA GPU with 8 GB VRAM or better
- Windows + LM Studio for first setup

This setup is practical, not cloud-fast.

## Recommended runtime order

1. LM Studio for Windows and Claude Code compatibility.
2. Ollama for terminal-first local workflows.
3. llama.cpp for direct GGUF control.
4. vLLM for later Linux/server experiments.

## LM Studio setup

1. Install LM Studio.
2. Set model directory to a large internal SSD.
3. Download Qwen3-Coder 30B-A3B Instruct GGUF Q4.
4. Load the model.
5. Start with context 8192 or 16384.
6. Start Local Server on `http://localhost:1234`.

## Claude Code local route

PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:1234"
$env:ANTHROPIC_AUTH_TOKEN = "lmstudio"
claude
```

Then run:

```text
/local_model_session
```

## Codex local route

Add a profile to `~/.codex/config.toml`:

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

## Smoke test

Ask the local model:

```text
You are running in LOCAL MODEL MODE.
Read AGENTS.md.
Read wiki/index.md.
Do not scan raw/.
Summarize the wiki structure in 10 bullets.
Then identify which two pages are relevant for a UR10e ROS2-Grasshopper question.
Do not edit files.
```

Pass condition:

- It reads rules first.
- It does not scan raw.
- It identifies relevant wiki pages.
- It does not invent files.
- It does not try to edit.

## Local model discipline

Local Qwen is powerful, but it needs tighter task boundaries. Use it like a skilled offline assistant, not an autonomous senior engineer.

Good tasks:

- explain a wiki page
- summarize raw into a wiki draft
- edit one Python file
- generate URScript formatting helpers
- review one ROS2 node
- compare DGL/PyG/SVM experiment structure

Avoid:

- whole-repo refactors
- autonomous robot motion changes
- broad package upgrades
- large raw ingestion in one pass
- claims about current APIs without Context7 or cached notes


## Long work with local Qwen

Qwen3-Coder 30B-A3B Q4 can support long work when the project state is written to files. Do not depend on one huge context window.

Use:

```text
outputs/YYYY-MM-DD/<task_slug>/PLAN.md
outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_001.md
outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_002.md
```

Claude Code command:

```text
/local_long_task <task-slug>
```

Codex prompt:

Use the "Local long task" prompt in `SETUP_PROMPTS.md`.

Recommended pattern:

1. Cloud Claude or Codex creates the first plan when available.
2. Local Qwen executes one chunk offline.
3. Local Qwen writes a checkpoint.
4. Later, cloud Claude or Codex reviews the checkpoint and diff.
5. Confirmed knowledge is promoted into `wiki/`.

This gives you uninterrupted travel workflow without forcing the local model to behave like a frontier cloud model.
