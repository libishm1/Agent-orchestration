# Compatibility across the three repositories

Three repositories share one working contract. An agent that reads one of them
should be able to work in any of them without relearning the rules.

| Repository | Role | Contract file | Skills folder |
|---|---|---|---|
| `Agent-orchestration` (this repo) | Orchestration template: memory layers, handoffs, audit trail, subagent roles | `project_context_template/AGENTS.md` (plus `CLAUDE.md`, `GEMINI.md`) | `.claude/agents/`, `.claude/commands/` |
| `computational-design-skill` | Agent skills: computational design, AI-assisted debugging, research synthesis, conversation handoff | `AGENTS.md` (plus `CLAUDE.md`) | `skills/<name>/` |
| `open-science` | Desktop research workbench. Bundles skills in its own format | `AGENTS.md` (plus `CLAUDE.md`) | `resources/skills/<name>/`, registered in `resources/skills/manifest.json` |

## What is shared

1. **One rules file per repo.** `AGENTS.md` holds the rules. `CLAUDE.md` imports it with
   `@AGENTS.md`. `GEMINI.md` points to it. Codex and local agents read `AGENTS.md`.
2. **One skill format.** A folder named after the skill, containing `SKILL.md` with
   frontmatter `name` (equal to the folder name) and a `description` that says when to use
   the skill. Optional `references/`, `templates/`, `scripts/`.
3. **One privacy rule.** No personal paths, names, client names, contact details or
   credentials in any file that leaves the machine. Use placeholders.
4. **One verification habit.** Each repo has a check that runs before a change is
   committed. The skills repo uses `scripts/validate_skills.py` and its unit tests.
   The open-science repo runs `packages/skills` tests. This template runs
   `audit_query.py` and the wiki health check.
5. **One review gate.** Work happens on a branch. A person approves the merge.

## Where they differ

- The orchestration template is a memory and workflow scaffold for a project. It is not a
  skill library.
- The skills repo is a library. It has no runtime.
- The open-science repo is an application. Its skills are loaded by the app. Changes there
  need its build and tests, and an install of its workspace packages.

## Using a skill from another repo

- Claude Code: copy the skill folder to `.claude/skills/` in the project, or to
  `~/.claude/skills/` for all projects.
- Codex: point the prompt at the `SKILL.md` path. Load `references/` on demand.
- Local models: load only the `SKILL.md` and the one reference the task needs.
- open-science: the bundled skills appear in the app's skill list.

## Keeping the three in step

- When a rule changes in one `AGENTS.md`, check the other two for the same rule.
- When a skill's format changes, update the validator in the skills repo, then the
  manifest in open-science.
- When a diagnostic role changes, update `docs/MULTI_AGENT_DIAGNOSTICS.md` here and the
  `ai-debugging` skill in both skill repos.

## Runtimes and hosts

- Herdr (`herdrdev/herdr`, Apache-2.0): a terminal runtime for coding agents, not an
  orchestration framework. Each pane is one agent. Panes report working, blocked or idle.
  Agents drive it through a CLI and socket API. Use one task card and one skill path per pane.
  Coordination logic stays in the task cards and in `EXTERNAL_ORCHESTRATORS.md`.
  Windows support is a beta. Verify CLI commands against your installed version.
- Omarchy: an Arch Linux setup with the Hyprland compositor. Skills and this template need
  no changes. Rhino and Grasshopper steps must run on Windows or macOS, or on a remote host.

## Known gaps

- The validator in the skills repo checks names and links. It does not check that the
  open-science manifest matches the folders. Check that by hand until a script exists.
- Tests in open-science that create symbolic links can fail on Windows without developer
  mode. This is an environment limit, not a skill defect.
