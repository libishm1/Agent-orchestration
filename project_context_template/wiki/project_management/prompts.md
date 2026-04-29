# Prompts

## Purpose

Calibrated prompts and writing-voice rules for this project. The assistant references this page from `AGENTS.md` when drafting or editing manuscripts, READMEs, or formal documents.

## Writing voice (for Libish's documents)

These rules apply to any document written *by the assistant on Libish's behalf*: papers, proposals, READMEs, formal emails, biodatas, statements.

### Core rules

- **Short declarative sentences.** 12–20 words is the anchor. Longer is fine when subordinate clauses carry essential technical detail.
- **Confident assertions.** No hedging weasel words ("it could be argued", "this might suggest", "it should be noted that"). When evidence is incomplete, bound the uncertainty explicitly.
- **Restate key points** as standalone sentences for emphasis. Use sparingly — once per major section, in Introduction or Discussion only.
- **"X, specifically Y" narrowing.** Introduce a broad concept, then narrow immediately. Example: *"Graph-based representations, specifically adjacency matrices encoding room connectivity, enable …"*
- **Frame technical contributions inside larger narratives.** Open with the problem. Close with what the contribution enables next.
- **Systems-thinking decomposition.** For complex systems: name each subsystem, show integration points.

### Strongly avoid

- "it is worth noting that" / "it should be noted that" — delete the wrapper, keep the content.
- "in order to" → "to".
- "utilize" → "use".
- "leverage" as a verb → "use", "exploit", "apply".
- "novel" without substantiation — say what makes it new.
- "state-of-the-art" without a specific named benchmark.
- Em dashes — replace with periods, semicolons, or commas.

### Auto-fix on edit

- Comma splices → period or semicolon.
- Fragments in body text → complete sentences. Fragments are fine in figure captions and table notes.
- Passive voice in Methods → active voice. Exception: when the agent is genuinely irrelevant ("Samples were cured at 60°C for 24 h").
- Inconsistent capitalization → enforce one convention.

### Flag, do not auto-fix

- Uncontextualized metrics — flag with "relative to what?".
- Unsubstantiated claims — flag, do not invent citations.
- "NP-Hard" without formal justification — suggest "computationally expensive" or "combinatorially complex".
- Sustainability claims without numbers or citations — flag.
- Limitations framed as apologies — suggest reframing as bounded scope.

## Reusable assistant prompts

### Draft a paper section

```
Use the academic-writing skill in Mode 1 (Draft).
Apply the voice rules in wiki/project_management/prompts.md.
Section: <Introduction | Methods | Results | Discussion | Abstract>
Inputs:
- Research question:
- Key data:
- Constraints:
- Target venue:
```

### Edit a paper section

```
Use the academic-writing skill in Mode 2 (Edit).
Apply the voice rules and correction rules in wiki/project_management/prompts.md.
Output: revised text + change log.
Do not change technical claims without explicit confirmation.
```

### Review a paper section

```
Use the academic-writing skill in Mode 3 (Review).
Categorize issues as ARGUMENT > EVIDENCE > STRUCTURE > VOICE > GRAMMAR > CITATION.
Do not rewrite. Flag only.
```

### Draft a robotics design note

```
Apply the voice rules in wiki/project_management/prompts.md.
Read wiki/ur10e_ros2_grasshopper/pose_frame_rules.md as the structural reference.
For any motion code: state execution level (1/2/3) and the safety gate.
For any pose: frame-tag every variable as <thing>_in_<frame>.
```

## Last updated

2026-04-29
