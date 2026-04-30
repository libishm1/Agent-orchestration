# Human Verification Checklist

## Purpose

Short checklist for medium, long, or high-risk work. Do not require this for tiny edits.

## Scope

- [ ] Task goal is clear.
- [ ] Task size is marked small, medium, or long.
- [ ] Allowed files to read are named.
- [ ] Allowed files to edit are named.
- [ ] Stop conditions are clear.

## File Safety

- [ ] `raw/` is not edited.
- [ ] Unrelated files are not changed.
- [ ] Generated outputs are kept in `outputs/YYYY-MM-DD/`.
- [ ] Durable memory is promoted to `wiki/` only after approval.

## Code Safety

- [ ] No package install is needed, or installation is explicitly approved.
- [ ] No destructive shell command is used.
- [ ] Verification method is defined before editing.
- [ ] Completion evidence is available or manual verification steps are written.

## Robotics Safety

- [ ] No robot motion command is run.
- [ ] UR10e with RG6 gripper pose units and frames are explicit.
- [ ] TCP pose and motion target pose are not mixed.
- [ ] Hardware use requires separate human approval.

## GraphML Validity

- [ ] Same nodes, features, split, metric, and seed are used for baseline comparisons.
- [ ] Leakage risks are checked.
- [ ] Claims are limited to the verified dataset and metric.

## Memory Promotion

- [ ] Confirmed facts and assumptions are separated.
- [ ] Evidence source is listed.
- [ ] Open questions are preserved.
- [ ] Wiki page remains concise.

## Task Completion Evidence

- [ ] Definition of Done is met.
- [ ] Diff summary is reviewed.
- [ ] Test, compile, script, or manual verification evidence is recorded.
- [ ] Any unverified claim is marked as unverified.

## Last updated

2026-04-30
