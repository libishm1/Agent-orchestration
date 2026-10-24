# Connecting an external orchestrator

This template does not depend on any specific orchestrator. An external tool (a
"herder", a CI job, a queue runner, or your own pipeline) can drive it if it respects the
file contract below. The contract is the interface. The tool's own API is not assumed.

> Herdr: the project owner describes Herdr as an AI agent orchestration framework.
> Web search results were inconsistent: some describe a terminal multiplexer for coding
> agents with a local socket API, and several GitHub copies exist (only one is likely
> canonical). The canonical repository, licence and supported-agent list are NOT confirmed
> here. Before connecting Herdr, read its official README, record the version, and add the
> verified commands to this page. Until then, follow the file contract below only.

## What the orchestrator provides

- A task card: `outputs/<YYYY-MM-DD>/<task_slug>/TASK.md` with the goal, the allowed files,
  the forbidden actions, the output target, and the verification method (see the prompt
  specificity rule in `AGENTS.md`).
- A working directory for the run.
- Permission scope: which commands may run without asking.

## What the orchestrator reads back

- `CHECKPOINT_<n>.md` after each chunk: completed work, files touched, open risks, the
  next command.
- `DIAG_STATUS.md` for a diagnostic run (see `MULTI_AGENT_DIAGNOSTICS.md`).
- Exit status of the verification commands, recorded in the output file.
- One event per milestone appended to `wiki/audit_trail.jsonl`.

## Hand-off between agents

Each step writes a handoff file and stops. The next step reads the file, not the previous
agent's context. Use these names:

- `HANDOFF_TO_CLOUD.md` (local to cloud)
- `HANDOFF_TO_QWEN.md` (cloud to local)
- `HANDOFF_TO_REVIEW.md` (any agent to a reviewer)

## Rules the orchestrator must keep

1. Do not let a step widen its own scope. A step that finds more work writes it to the
   plan and stops.
2. Keep the human gates from `AGENTS.md`. The orchestrator may propose a commit, a push,
   an install, or a launch. A person approves it.
3. Run every step on a branch. Merge only after review.
4. Record the agent name and role in the audit event.
5. Stop on the first failed verification. Do not retry in a loop.

## Minimal example (any tool)

```text
1. Orchestrator writes TASK.md and creates the run folder.
2. Planner step reads TASK.md and the routing table in AGENTS.md, writes PLAN.md, stops.
3. Human approves PLAN.md (gate).
4. Investigator step reproduces, writes evidence/*.md, writes CHECKPOINT_1.md, stops.
5. Fixer step applies the approved change, writes CHECKPOINT_2.md, stops.
6. Verifier step re-runs the checks, writes verify.md, appends the audit event.
7. Orchestrator reads verify.md. If it passed, it opens a review branch. If not, it
   returns to step 4 with the new evidence.
```

## Testing the connection

Run one step on a throwaway task first. Check that the files appear where the contract
says, that the audit event is written, and that no step widened its scope.
