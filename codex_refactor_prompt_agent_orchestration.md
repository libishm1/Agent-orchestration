# Codex Refactor Prompt for Agent Orchestration Repo

Use this prompt in Codex to refactor the `Agent-orchestration` repository. It consolidates the recommendations from the recent review: human verification, prompt specificity, Gemini support, context-budget discipline, positioning against open-source orchestrators, and task-completion verification.

```text
Read AGENTS.md first.

Task: Refactor this orchestrator repo to add human verification, prompt specificity, Gemini support, context-budget discipline, clearer positioning against open-source agent frameworks, and task-completion verification without overengineering it.

Goal:
Keep the repo lightweight. This should remain a practical project-memory and handoff scaffold, not a full agent framework.

Core positioning:
This repo is not trying to replace LangGraph, CrewAI, AutoGen, OpenHands, Cline, Roo Code, Claude Code templates, Qwen Code, Codex, Gemini, or other mature agent frameworks.

Position it as:
“A lightweight project-memory and handoff scaffold for multi-agent coding workflows.”

Alternative wording:
“A human-verifiable context protocol for Claude Code, Codex, Gemini, and local Qwen workflows.”

Avoid wording like:
- agent orchestration framework
- production-ready autonomous agent system
- replacement for LangGraph/CrewAI/Cline/Roo
- fully automated multi-agent platform

Core principle:
Human verification should reduce scope, not add ceremony.
Agents propose, inspect, summarize, patch, and verify.
Humans approve scope, diffs, durable memory, dependency installs, robot-related logic, physical fabrication decisions, academic claims, and any git commit or push.

Important framing:
Human-in-the-loop is not automatically token-efficient.
It becomes token-efficient only when it narrows what the agent reads, edits, verifies, and saves.
For small tasks, use a compact approval instruction.
For medium or high-risk tasks, use a short proposal first.
For long tasks, use checkpoints and handoffs.
For coding tasks, define success before editing.

Open-source comparison framing:
Add a concise README section explaining that this repo is a memory and handoff layer, not the execution engine.

Use this comparison logic:
- LangGraph, CrewAI, AutoGen, and similar frameworks do programmable multi-agent execution better.
- OpenHands, Cline, Roo Code, Continue, Qwen Code, Claude Code, Codex, and Gemini do actual coding-agent execution better.
- This repo provides durable project memory, human verification, explicit context routing, task verification, and handoff continuity across those tools.
- The intended stack is:
  - Claude Code = deep planning and review
  - Codex = cloud patch worker
  - Gemini = long-context scout and summarizer
  - Qwen Code = offline local execution
  - Roo/Cline/Continue = optional VS Code local-model execution
  - This repo = shared memory, prompts, handoffs, checkpoints, and verification contracts

Refactor requirements:

1. Add a Human Verification Layer

Add a concise section to AGENTS.md and README.md:

- Agents may propose, draft, inspect, summarize, patch, and verify.
- Humans approve:
  - task scope
  - files to edit
  - dependency installation
  - robot motion logic
  - physical fabrication decisions
  - durable wiki memory
  - git commits or pushes
  - claims used in academic writing
- No agent output becomes project truth until verified and promoted into wiki/.
- Human verification should reduce scope, not add ceremony.
- Use the checklist only for medium, long, or high-risk tasks.
- For small tasks, a single approval instruction is enough.

2. Add a Prompt Specificity Rule

Add a compact rule to AGENTS.md:

Every non-trivial task should specify:
- agent mode: Claude cloud / Codex cloud / Gemini cloud / Qwen local
- task size: small / medium / long
- allowed files to read
- allowed files to edit
- forbidden actions
- output target: chat only / outputs/YYYY-MM-DD/ / wiki after approval
- verification method: diff, test command, checklist, human approval, Context7 check, or manual verification

Also add this discipline:
- The prompt should narrow context before work starts.
- Do not force full wiki/session workflows for small tasks.
- Do not run health checks unless the task asks for wiki maintenance or a long-task review.
- Do not read all raw/ or all wiki/ unless the user explicitly asks for ingestion or audit.

3. Add Gemini as a fourth agent lane

Add a root GEMINI.md file.

Keep it thin. It should import AGENTS.md if supported, or tell Gemini to read AGENTS.md first.

Gemini role:
- long-context reader
- repo summarizer
- wiki assistant
- handoff generator
- contradiction scanner
- documentation drafter

Gemini should not be final authority for:
- UR10e motion safety
- robot execution decisions
- physical fabrication safety
- dependency installation
- git push
- destructive shell commands

Add Gemini to the Agent Mode Matrix:
- Claude Code cloud = planning, hard reasoning, safety review
- Codex cloud = patch-oriented coding and PR-style work
- Gemini cloud = long-context inspection and summarization
- Qwen local = offline checkpoint execution worker

4. Add one human verification checklist only

Create:
wiki/project_management/human_verification_checklist.md

Keep it short and practical.

Include sections:
- scope
- file safety
- code safety
- robotics safety
- GraphML validity
- memory promotion
- task completion evidence

Do not create multiple governance documents.
Do not make the checklist mandatory for every small task.

5. Add prompt templates without bloating the repo

Add or update SETUP_PROMPTS.md with these reusable templates:

A. Small task prompt:
- read AGENTS.md
- read only the target file
- do not update wiki
- do not create checkpoint
- edit only approved file
- show diff and test command or state why no test applies

B. Before editing:
Ask the agent to produce an edit proposal first:
- task interpretation
- files to read
- files to edit
- expected output
- risks
- verification contract
- test command or manual verification method
- what needs human approval
No edits yet.

C. Proceed after approval:
- edit only approved files
- do not install packages
- do not edit raw/
- do not git push
- do not run robot motion commands
- save patch summary to outputs/YYYY-MM-DD/ only if useful
- show diff
- run agreed verification if safe
- state whether Definition of Done was met

D. Review local Qwen checkpoint:
- read PLAN.md
- read CHECKPOINT_N.md
- read git diff
- verify scope, file safety, assumptions, and whether cloud review is needed
- check whether the checkpoint met its Definition of Done
- do not edit yet

E. Promote memory to wiki:
- propose wiki path
- separate confirmed facts from assumptions
- list unresolved questions
- state evidence source
- do not write until human approval

F. Specific task template:
Include fields:
Agent mode:
Task size:
Task:
Allowed to read:
Allowed to edit:
Do not:
Use:
Verification:
Definition of Done:
Stop conditions:

G. Verification contract template:
Include fields:
Task:
Definition of Done:
Expected change:
Allowed verification:
Completion evidence required:
Stop if:

6. Keep context-budget discipline

Make sure README.md and AGENTS.md clearly state:

Small task:
- read AGENTS.md and target file only
- no wiki update
- no checkpoint
- no health check
- one compact approval instruction is enough
- verification can be diff-only if the task is documentation-only

Medium task:
- read AGENTS.md
- read wiki/index.md
- read 1 to 3 relevant wiki pages
- save one output summary if useful
- ask before promoting memory to wiki
- define a verification contract before editing

Long task:
- use PLAN.md
- use CHECKPOINT_N.md
- use handoff prompts
- use selective wiki updates
- run checklist if risk is high
- run health check only when relevant
- define checkpoint-level Definition of Done

Do not make every task use the full workflow.

7. Add open-source comparison without scope creep

Add a concise section to README.md, not a huge comparison table.

Suggested title:
“How this compares to agent frameworks”

Content should say:
- This repo is not a full orchestrator.
- It does not schedule agents, manage state graphs, run sandboxed autonomous tasks, or replace coding agents.
- It complements existing tools by providing a shared project-memory, verification, and handoff layer.
- Use LangGraph/CrewAI/AutoGen when you need programmable multi-agent execution.
- Use Cline/Roo/Continue/Qwen Code/Claude Code/Codex/Gemini when you need actual coding execution.
- Use this repo when you need continuity, human verification, context routing, task verification, and online/offline handoffs across tools.

8. Add task completion verification

Add a lightweight verification contract system.

Update AGENTS.md and SETUP_PROMPTS.md with:

A. Definition of Done rule
For every non-trivial coding task, define success before editing.

A task is complete only when the agent can show evidence that the expected outcome was achieved.

The verification contract must include:
1. Goal
   - What should be true after the task?
2. Expected change
   - Which behavior, file, function, command, or output should change?
3. Verification method
   - Test command
   - Type check
   - Lint
   - Unit test
   - Script execution
   - Diff inspection
   - Output file existence check
   - Manual checklist
   - Human approval
4. Evidence
   - Command output
   - Test result
   - Diff summary
   - Generated file path
   - Before/after behavior
   - Error message resolved
5. Stop condition
   - When should the agent stop instead of continuing?
   - Examples:
     - test fails for unrelated dependency
     - required file is missing
     - task needs package installation
     - robot execution would be required
     - assumptions are unsafe or unverified

Agents must not claim a task is complete without verification evidence.
If verification cannot be run, the agent must say so and provide exact manual verification steps.

B. Tool Call Verification rule
When an agent calls a tool, the tool result must be checked against the task goal.

For every meaningful tool call, record:
- Tool called
- Input summary
- Expected result
- Actual result
- Verification status:
  - passed
  - failed
  - partial
  - not verifiable
- Next action

If the tool result is partial or ambiguous, the agent must not treat the task as complete.

Example:
Tool: pytest
Expected: all tests in tests/test_parser.py pass
Actual: 7 passed, 1 failed
Status: failed
Next action: inspect failing test before claiming completion

C. Verification Levels
Add simple verification levels:

V0: Diff-only verification
Use for documentation or tiny edits.
Evidence: changed files and diff summary.

V1: Static verification
Use for syntax-sensitive changes.
Evidence: lint, type check, import check, or compile check.

V2: Runtime verification
Use for code behavior changes.
Evidence: unit test, script run, CLI output, generated file, or before/after result.

V3: Human-in-loop verification
Use for robotics, fabrication, academic claims, or safety-critical decisions.
Evidence: agent output plus human approval.

Recommended minimum verification:
- README edit = V0
- Python syntax fix = V1
- ROS2 node change = V1 or V2
- Grasshopper Python code = V1 if possible, otherwise V3 manual verification
- URScript waypoint generation = V2 + V3
- Robot motion logic = V3 only, no execution
- GraphML experiment script = V2
- Wiki memory promotion = V3

9. Add verification prompt behavior

Add to SETUP_PROMPTS.md:

Before coding:
Read AGENTS.md.
Before editing, write a verification contract.
Include:
1. goal
2. expected change
3. files likely affected
4. verification method
5. evidence required to claim completion
6. stop conditions
Do not edit until the verification contract is clear.

After editing:
1. run the agreed verification method if safe
2. show command output or explain why it could not be run
3. summarize the diff
4. state whether the Definition of Done was met
5. do not claim completion without evidence

10. Avoid overengineering

Do not add:
- new agent framework code
- vector database
- complex automation
- many new folders
- duplicate governance files
- redundant prompts
- CI unless already present
- multiple versions of the same checklist
- mandatory checklist gates for small edits
- long open-source comparison tables
- a custom test framework
- programmatic workflow engine

Prefer editing existing files over creating new ones.
Prefer short sections over long policy documents.

11. File changes expected

Likely edit:
- README.md
- AGENTS.md
- SETUP_PROMPTS.md
- wiki/index.md if needed
- wiki/local_ai_workflow/handoff_workflows.md if needed

Likely create:
- GEMINI.md
- wiki/project_management/human_verification_checklist.md

Do not touch:
- raw/
- unrelated example files
- generated outputs unless needed for documentation

12. Output

Before editing, show a short refactor plan.

After editing, provide:
- files changed
- why each change was made
- where token/context overhead was reduced
- what overengineering was avoided
- how the repo is now positioned relative to open-source agent frameworks
- how task-completion verification was added
- remaining TODOs

Do not run package installs.
Do not git push.
Do not edit raw/.
```
