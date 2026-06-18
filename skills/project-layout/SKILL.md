---
name: project-layout
description: Define and enforce the shared project artifact path contract for documentation, plans, work notes, immutable references, research repositories, and generated publications. Use when creating or reorganizing a project, choosing where a durable artifact belongs, resolving competing folder conventions, or updating another skill that creates project files.
---

# Project Layout

Use this contract for project-level artifacts. Treat paths as relative to the project root, normally the Git worktree root. Do not infer the root from the current working directory when a repository root can be discovered.

## Canonical Paths

| Path | Purpose |
| --- | --- |
| `docs/` | Durable, maintained project knowledge: manuals, design documentation, decisions, and other material that describes the project as it is. Markdown and HTML are both valid. |
| `docs/wiki/` | An LLM-maintained or interlinked knowledge base when the project needs one. |
| `docs/public/` | Portable publication output, including generated HTML reports or research publications. |
| `plans/` | Work state, direction, and planning history. |
| `plans/to-do/` | Draft or queued work that has not started. |
| `plans/in-progress/` | Active work that must survive across sessions. Keep one durable plan or journal per workstream. |
| `plans/completed/` | Finished plans retained as history. Name completed files `YYYY-MM-DD-<slug>.md`. |
| `plans/notes/` | Exploratory project notes, notebooks, hunches, and long-term guidance that are not authoritative documentation or source evidence. |
| `ref/` | External source material and reference inputs. Treat accepted source files as immutable; maintain provenance manifests alongside them when needed. |

Keep repository control files such as `README.md`, `AGENTS.md`, `CLAUDE.md`, `LICENSE`, and ecosystem configuration at the root when their tools expect that location.

Source-code paths such as `src/`, `tests/`, package-local `assets/`, and repository utilities such as `scripts/` follow ecosystem conventions. They are outside this artifact contract. Paths inside an installed skill, such as its own `scripts/`, `references/`, or `assets/`, are also outside this contract.

When authoring or updating another skill, use this contract for every project artifact that skill creates. State specialized paths as children of the canonical roots. Mention a legacy path only for discovery or migration; do not present it as an equal creation option.

## Path Resolution Rules

1. Inspect the repository before creating a path.
2. Use an existing canonical path when present.
3. If the repository has one established legacy equivalent, keep using it for the current task rather than creating a parallel tree. Recommend or perform migration only when the user requests reorganization or the task explicitly includes it.
4. In a new project, or when no equivalent exists, create the canonical path.
5. Never split one artifact class across canonical and legacy paths.
6. Write documented paths from the project root with `/` separators. Resolve them to native filesystem paths only when executing commands.

Recognize these legacy equivalents, but do not introduce them in new projects:

| Legacy path | Canonical destination |
| --- | --- |
| `doc/` | `docs/` |
| `wiki/` | `docs/wiki/` |
| `corpus/` | `docs/public/` |
| `plan/` | `plans/` |
| `todos/`, `tasks/`, `plans/todos/` | `plans/to-do/` |
| `notebook/`, `scratchpad/`, `thoughts/`, `notes/` | `plans/notes/` |
| `raw/`, `reference/` | `ref/` |
| `ingest/` | `plans/in-progress/ingest/` |

## Plan Lifecycle

- Draft a new workstream in `plans/to-do/<slug>.md` when planning must be preserved before implementation.
- Move its file to `plans/in-progress/<slug>.md` when work starts; append progress and decisions there instead of creating session-specific notes elsewhere.
- Move it to `plans/completed/YYYY-MM-DD-<slug>.md` when the work is complete.
- Keep non-status notes in `plans/notes/`; do not move them through the work lifecycle.
- Update links when moving a plan. Do not leave duplicate copies behind.

For a greenfield scaffold, create only the canonical directories the project actually needs. Use `.gitkeep` only to retain an otherwise empty directory in Git; remove it when real content is added.
