---
description: Run a multi-agent diagnosis of a failure. Plans the run, then reproduces, captures evidence, reviews by layer, fixes only the approved change, and verifies. Use when a single-agent attempt did not isolate the cause.
---

Read CLAUDE.md and `docs/MULTI_AGENT_DIAGNOSTICS.md`.

Symptom: $ARGUMENTS

1. Create `outputs/<today>/diag_<slug>/` and write `DIAG_PLAN.md` with the symptom, environment, suspected layers, roles, and stop rule. Use the diagnostic-coordinator subagent for this step.
2. Ask the user to approve the plan before any fix.
3. Run the debug-investigator subagent to reproduce and capture evidence. Save every evidence file with the standard header.
4. Run the coordinator again to decide the root cause, or to request one more capture.
5. Apply the approved fix in the smallest set of files. Stop if more than five files change.
6. Re-run the reproduction and the regression checks in a separate step. Record the output in `verify.md`.
7. Write `DIAG_STATUS.md` and append a `task_complete` or `checkpoint` event to `wiki/audit_trail.jsonl`.
