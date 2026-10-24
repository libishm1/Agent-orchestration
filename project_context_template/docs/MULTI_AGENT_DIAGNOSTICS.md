# Multi-agent diagnostics

A protocol for diagnosing a failure with several agents, each in a bounded role, with
evidence passed between them as files. It works with Claude Code subagents, Codex, a
local model run in sequence, or an external orchestrator. Read this with `AGENTS.md`.

## When to use it

Use the multi-agent path when at least one of these is true:

- The failure spans more than one layer (application, library, runtime, native code,
  host application, environment).
- A first single-agent attempt did not reproduce or isolate the cause.
- Evidence must be captured in a live tool (debugger, profiler, host app) and reviewed
  separately.
- The fix will touch a validated approach, a safety gate, or a shared contract.

Use a single agent for a one-line fix, a failing unit test with a clear message, or a
question answered by reading one file.

## Roles

| Role | Job | Writes | Does not |
|---|---|---|---|
| Coordinator | Splits the work, sets the order, collects the outputs, decides when to stop | `DIAG_PLAN.md`, `DIAG_STATUS.md` | Debug or edit code |
| Investigator | Reproduces the failure, captures evidence, forms hypotheses | `evidence/*.md`, a minimal repro | Change production code |
| Layer reviewer | Checks one layer against its rules (robotics, GraphML, native interop, API use) | `reviews/<layer>.md` | Edit files |
| Fixer | Makes the smallest change that the coordinator approved | the code change, `fix_notes.md` | Widen scope past the approved change |
| Verifier | Re-runs the repro and the regression checks, separately from the fixer | `verify.md` | Fix the bug it finds |

One agent can play several roles when the tool has no subagents. Keep the outputs in
separate files so a reader can tell who said what. The verifier must not be the fixer
in the same pass when a second agent or a second session is available.

## Procedure

1. **Plan (coordinator).** Write `DIAG_PLAN.md` with: symptom in one sentence, the
   environment, the layers suspected, the roles to run, and the stop rule.
2. **Reproduce (investigator).** Make the failure happen with the smallest input. Save the
   command, input, and output. A failure that is not reproduced is not yet diagnosed.
3. **Capture (investigator).** Collect the evidence the layer needs: stack trace,
   sanitizer report, loaded modules, log lines at a boundary, or a minidump. Name each
   file. Do not paraphrase a trace in place of saving it.
4. **Hypothesise (investigator).** Write one or more hypotheses. For each, name the test
   that would falsify it.
5. **Review (layer reviewers).** Each reviewer reads the evidence for its layer and
   answers: does the evidence support the hypothesis, what rule applies, what is missing.
6. **Decide (coordinator).** Pick the root cause, or ask for one more capture. Write the
   decision and the reason in `DIAG_PLAN.md`.
7. **Fix (fixer).** Change the smallest set of files. Stop and ask before touching more
   than five files or any gate listed in `AGENTS.md`.
8. **Verify (verifier).** Re-run the reproduction and the regression checks. Record the
   output. A passing test is not enough when the truth criterion needs a visual check.
9. **Close (coordinator).** Write `DIAG_STATUS.md` with the outcome, open risks, and the
   next command. Append a `task_complete` or `checkpoint` event to the audit trail.

## Evidence format

Every evidence file starts with this header:

```markdown
# Evidence: <short title>
- Date:
- Agent role:
- Environment: OS, runtime or compiler version, host version, bitness
- Reproduction command or steps:
- Input file(s):
- Hypothesis tested:
- Result: supports | refutes | inconclusive
- Raw output file:
```

Raw output goes in a file next to the note. Quote only the lines the conclusion needs.

## Stop rules

- Stop and report when two captures in a row give no new information.
- Stop and ask before any command that attaches to, kills, or launches an interactive
  application, or that touches hardware.
- Stop when the fix would change a validated approach. Quote the wiki entry first.
- Stop when the cost of the next step is larger than its expected information.

## Guardrails

- Do not kill a process by image name when several may be running. Identify the process
  ID first.
- Do not claim a root cause from a green build alone.
- Mark every version-specific command as `verify:` and check it against `--help` or the
  official docs before using it.
- Keep secrets, personal paths and contact details out of evidence files. Use placeholders.

## Compatibility

The same files work in every tool:

- Claude Code: the coordinator and investigator are subagents in `.claude/agents/`. Invoke
  them with `/diagnose`.
- Codex: read `AGENTS.md`, then run the roles in sequence as separate prompts.
- Local models: run one role per session. Pass the previous file's path, not its contents,
  to keep the context small.
- External orchestrators: see `EXTERNAL_ORCHESTRATORS.md`.

## Related

- `.claude/agents/diagnostic-coordinator.md`
- `.claude/agents/debug-investigator.md`
- `.claude/commands/diagnose.md`
- `docs/COMPATIBILITY.md`
- Skill: `ai-debugging` (in the computational-design skill suite and the open-science bundle)
