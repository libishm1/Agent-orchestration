# Qwen Code Offline

## Purpose

This page defines the offline coding workflow using Qwen Code with a local Qwen model. Use this when travelling, flying, when Claude limits expire, or when internet access is unstable.

## Confirmed facts

Qwen Code is an open-source terminal coding agent optimized for Qwen models. It supports interactive terminal use, headless mode, IDE integration, and local model endpoints through OpenAI-compatible providers.

For local mode, configure `~/.qwen/settings.json` with `modelProviders` and a local `baseUrl`, such as Ollama `http://localhost:11434/v1` or vLLM `http://localhost:8000/v1`.

## Recommended offline stack

Preferred:

```text
VS Code
Qwen Code CLI / VS Code integration
LM Studio or Ollama local server
Qwen3-Coder 30B-A3B Q4 or closest available local coding model
AGENTS.md + wiki + outputs checkpoint protocol
```

Fallback:

```text
LM Studio chat
Same repo files
Manual prompts from outputs/.../QWEN_PROMPT_N.md
```

## Local provider examples

### Ollama-style OpenAI-compatible endpoint

```json
{
  "modelProviders": {
    "openai": [
      {
        "id": "qwen3-coder-30b-local",
        "name": "Qwen3-Coder 30B Local",
        "envKey": "OPENAI_API_KEY",
        "baseUrl": "http://localhost:11434/v1",
        "description": "Local Qwen coding model via Ollama-compatible endpoint"
      }
    ]
  },
  "env": {
    "OPENAI_API_KEY": "local-not-used"
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "model": {
    "name": "qwen3-coder-30b-local"
  }
}
```

### vLLM-style OpenAI-compatible endpoint

```json
{
  "modelProviders": {
    "openai": [
      {
        "id": "Qwen/Qwen3-Coder-30B-A3B-Instruct",
        "name": "Qwen3-Coder 30B local vLLM",
        "envKey": "OPENAI_API_KEY",
        "baseUrl": "http://localhost:8000/v1",
        "description": "Local Qwen model via vLLM"
      }
    ]
  },
  "env": {
    "OPENAI_API_KEY": "local-not-used"
  },
  "security": {
    "auth": {
      "selectedType": "openai"
    }
  },
  "model": {
    "name": "Qwen/Qwen3-Coder-30B-A3B-Instruct"
  }
}
```

## Offline session start

Paste this into Qwen Code:

```text
Read AGENTS.md.
Read wiki/index.md.
Read the latest 5 entries of wiki/log.md.
Read wiki/health.md.

Active mode: Qwen Code offline local model.
No Context7. No internet assumptions.
Use wiki notes first. Mark API-sensitive claims as stale if needed.

Summarize:
1. 3 most relevant wiki pages
2. latest checkpoint if any
3. risks before editing
Then wait.
```

## Offline execution prompt

```text
Read AGENTS.md.
Read wiki/index.md.
Read only the wiki pages needed for this task.

You are in Qwen Code offline mode.
Complete only the next checkpoint.
Do not read the whole repo.
Do not run package installs.
Do not edit raw/.
Do not run robot motion commands.

Task: [paste task]

Save progress to outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_N.md.
End with the exact next prompt to continue.
```

## What Qwen Code should do offline

Good tasks:

- small code edits
- URScript formatting
- Grasshopper Python cleanup
- selected-file reviews
- wiki queries
- checkpoint execution
- documentation drafts
- test-plan writing

Avoid offline unless a cloud model already planned it:

- whole-repo refactors
- ambiguous architecture changes
- large dependency migrations
- safety-critical robot execution
- unsupported API updates

## Query workflow

1. Read `wiki/index.md`.
2. Read only relevant wiki pages.
3. Read selected raw files only if wiki is missing.
4. Answer.
5. Save reusable answer to `outputs/YYYY-MM-DD/`.
6. Ask where to promote durable memory when back online or with human review.

## Last updated

2026-04-29
