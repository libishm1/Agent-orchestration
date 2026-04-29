# /local_long_task <task-slug>

Read CLAUDE.md.

You are running a long task in LOCAL MODEL MODE. Use this command when the active model is Qwen3-Coder or another local model.

Task slug: $ARGUMENTS

Workflow:

1. Read `wiki/index.md`.
2. Read the last 5 entries of `wiki/log.md`.
3. Create or update `outputs/YYYY-MM-DD/$ARGUMENTS/PLAN.md`.
4. Break the task into small chunks.
5. Work on only the first chunk.
6. Write `CHECKPOINT_001.md` or the next checkpoint number.
7. Include completed work, files read, files changed, risks, and the exact next command.
8. Do not scan raw unless explicitly asked.
9. Do not edit more than one code file or one wiki page in this chunk.

End by asking whether to continue with the next checkpoint.
