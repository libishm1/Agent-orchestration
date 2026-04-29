Read CLAUDE.md first.

Review local Qwen work and prepare a cloud review.

Input:
$ARGUMENTS

Read:
- relevant HANDOFF_TO_QWEN.md
- relevant TASK_PLAN.md
- latest CHECKPOINT_N.md
- changed files listed in the checkpoint

Check:
1. correctness
2. API compliance
3. robotics or GraphML constraints
4. missing tests
5. wiki updates needed

Use Context7 only for current API claims.
Return a concise review and save reusable findings to outputs/YYYY-MM-DD/.
