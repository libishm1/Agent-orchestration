# Setup Prompts

These prompts are for first-time setup and for Codex (which does not have slash commands).
Claude Code users can use the slash commands in `.claude/commands/` instead.

## First-time setup (Codex)

```text
Read AGENTS.md first.

Set up the project memory folders if missing:
- raw/ with subfolders ur10e_ros2_grasshopper, graphml_baseline_comparison, local_ai_codex_claude, fabrication_workflows, references, 00_inbox
- wiki/ with subfolders ur10e_ros2_grasshopper, graphml_baseline_comparison, local_ai_workflow, project_management
- outputs/

Verify these top-level wiki files exist:
- wiki/index.md
- wiki/log.md
- wiki/health.md
- wiki/glossary.md

Do not ingest raw content yet.
Show the file tree and report any missing files.
```

## First-time setup (Claude Code)

```text
Read CLAUDE.md first.
Run the equivalent of /session_start.

Verify the wiki structure exists:
raw/, wiki/, outputs/, .claude/agents/, .claude/commands/
wiki/index.md, wiki/log.md, wiki/health.md, wiki/glossary.md

Do not ingest raw content yet.
Show the file tree and confirm subagents are registered.
```

## Session start (Codex)

```text
Read AGENTS.md.
Read wiki/index.md.
Read the last 5 entries of wiki/log.md.
Read wiki/health.md.

Summarize:
1. The 3 most recently touched wiki pages.
2. Any P0 contradictions in health.md.
3. Open questions older than 14 days.

Then wait for the next instruction.
```

## Ingest (Codex)

```text
Read AGENTS.md.

Ingest raw material into wiki using the rules in AGENTS.md.

Read wiki/index.md first.
Process up to 5 raw files at a time.
Do not edit raw.
Create or update only relevant wiki pages.
Update wiki/health.md with any contradictions, tagged P0/P1/P2.
Append to wiki/log.md.

Focus on:
1. UR10e ROS2-Grasshopper integration
2. GraphML baseline comparison (DGL/PyG vs SVM)
3. Local AI workflow with Context7, Codex, Claude Code, local models

At the end report:
1. Files created
2. Files updated
3. Contradictions found
4. Open questions
5. Next recommended ingest task
```

## Query (Codex)

```text
Read AGENTS.md.

Question:
[PASTE QUESTION]

Workflow:
1. Read wiki/index.md.
2. Read only the relevant wiki pages.
3. Read raw only if the wiki is missing, stale, or contradictory.
4. Use Context7 only for current API documentation.
5. Save reusable answers to outputs/YYYY-MM-DD/.
6. Ask where to save durable memory.
```

## Health check (Codex)

```text
Read AGENTS.md.

Health check the wiki:
- missing linked pages
- orphan pages
- contradictions (tag P0/P1/P2)
- stale API claims (older than 90 days)
- concepts missing their own page
- outputs that should be promoted to wiki

Use Context7 only for API-sensitive claims.
Update wiki/health.md.
Append to wiki/log.md.
Suggest 3 new articles.
```

## Save memory (Codex)

```text
Read AGENTS.md.

Save durable memory from the last answer to: <wiki-path>

Rules:
- Save only durable, reusable knowledge.
- Separate confirmed facts from assumptions.
- Add links to related wiki pages.
- Append to wiki/log.md.
```


## Local long task (Codex or Claude local Qwen)

```text
Read AGENTS.md first.

You are running in LOCAL MODEL MODE.
Task slug: <task-slug>

Workflow:
1. Read wiki/index.md.
2. Read the last 5 entries of wiki/log.md.
3. Create or update outputs/YYYY-MM-DD/<task-slug>/PLAN.md.
4. Break the task into chunks.
5. Work on only the first chunk.
6. Do not edit more than one code file or one wiki page in this chunk.
7. Write outputs/YYYY-MM-DD/<task-slug>/CHECKPOINT_001.md or the next checkpoint number.
8. Include completed work, files read, files changed, risks, tests run, and the exact next command.
9. Do not scan raw unless explicitly asked.
10. Do not edit raw.

End by asking whether to continue with the next checkpoint.
```

## Handoff from local Qwen to cloud Claude/Codex

```text
Read AGENTS.md first.

Review the latest local-model checkpoint at:
outputs/YYYY-MM-DD/<task-slug>/CHECKPOINT_N.md

Tasks:
1. Verify the stated files changed.
2. Review the diff.
3. Use Context7 for API-sensitive code.
4. Identify mistakes or hallucinated API calls.
5. Produce a corrected next-step plan.
6. Save review notes to outputs/YYYY-MM-DD/<task-slug>/CLOUD_REVIEW.md.

Do not rewrite the whole task. Review and stabilize the local work.
```


## Qwen Code offline prompt

Paste into Qwen Code when working offline:

```text
Read AGENTS.md.
Read wiki/index.md.
Read the latest 5 entries of wiki/log.md.
Read wiki/health.md.

Active mode: Qwen Code offline local model.
No Context7. No internet assumptions.
Use wiki notes first. Mark API-sensitive claims as stale if needed.

Question or task:
[PASTE TASK]

Complete only the next checkpoint.
Save progress to outputs/YYYY-MM-DD/<task_slug>/CHECKPOINT_N.md.
End with the exact next prompt to continue.
```

## Resilient handoff prompts

### Prepare offline Qwen work

```text
Read AGENTS.md first.
Prepare a handoff for local Qwen Code.
Create outputs/YYYY-MM-DD/HANDOFF_TO_QWEN.md and TASK_PLAN.md.
Do not implement yet.
```

### Execute offline checkpoint

```text
Read AGENTS.md first.
Read HANDOFF_TO_QWEN.md and TASK_PLAN.md.
Complete only the next checkpoint.
Save CHECKPOINT_001.md.
End with the exact next prompt.
```

### Review local work in cloud

```text
Read AGENTS.md first.
Review the latest Qwen checkpoint.
Use Context7 only for current API documentation.
Return accept, minor edits, redo, or promote to wiki.
```
