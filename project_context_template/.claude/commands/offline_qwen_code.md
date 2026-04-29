# /offline_qwen_code <task>

Read CLAUDE.md.

Prepare this task for offline Qwen Code execution.

Task: $ARGUMENTS

Create an output folder under `outputs/YYYY-MM-DD/<task_slug>/` containing:

1. `PLAN.md` with small checkpoints.
2. `QWEN_PROMPT_001.md` with the exact first prompt to paste into Qwen Code.
3. A list of wiki pages Qwen should read.
4. A list of files Qwen may edit.
5. A list of files Qwen must not edit.

Use local-model-coordinator.
Do not edit project code in this command.
