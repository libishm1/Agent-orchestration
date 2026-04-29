# /qwen_checkpoint <task_slug>

Read CLAUDE.md.

You are preparing work for local Qwen continuation.

Task slug: $ARGUMENTS

Workflow:
1. Read `wiki/index.md`.
2. Read `outputs/YYYY-MM-DD/$ARGUMENTS/PLAN.md` if it exists.
3. Read the latest `CHECKPOINT_N.md` if it exists.
4. Complete only the next checkpoint.
5. Save progress to `outputs/YYYY-MM-DD/$ARGUMENTS/CHECKPOINT_N.md`.
6. End with the exact next prompt to continue in Qwen Code.

Constraints:
- one code edit per turn
- one wiki page update per turn
- no whole-repo edits
- no Context7 if offline
