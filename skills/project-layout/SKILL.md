---
name: project-layout
description: Define and enforce the standard project paths for documentation, plans, notes, references, research, and publications. Use when creating or organizing a project or when another skill creates durable project artifacts.
---

# Project Layout

Treat all paths as relative to the project root, normally the Git worktree root. Use this layout for new work; do not introduce alternative paths.

| Path | Purpose |
| --- | --- |
| `docs/` | Maintained project documentation and knowledge. |
| `docs/wiki/` | Interlinked or LLM-maintained knowledge base. |
| `docs/public/` | Portable publication output. |
| `plans/to-do/` | Draft or queued work. |
| `plans/in-progress/` | Active work that must survive across sessions. |
| `plans/completed/` | Finished plans retained as history. |
| `plans/notes/` | Exploratory notes, notebooks, and long-term guidance. |
| `ref/` | Immutable external sources and reference inputs. |
| `ref/inbox/` | The one mutable lane under `ref/`: staging for sources awaiting placement. Files become immutable once moved into `ref/`. |

Keep tool-required files such as `README.md`, `AGENTS.md`, `CLAUDE.md`, `LICENSE`, and ecosystem configuration at the root.

Source paths such as `src/`, `tests/`, package assets, repository utilities, and files inside an installed skill follow their own ecosystem conventions.

When a skill creates a durable project artifact, place it under these paths.

## Legacy Equivalents

Use the canonical paths for new work. On an existing project, recognize these legacy names and keep using one established tree rather than creating a parallel canonical one. Migrate only when the user asks or the task includes reorganization; never split one artifact class across canonical and legacy paths.

| Legacy path | Canonical destination |
| --- | --- |
| `doc/` | `docs/` |
| `wiki/` | `docs/wiki/` |
| `corpus/` | `docs/public/` |
| `plan/` | `plans/` |
| `todos/`, `tasks/`, `plans/todos/` | `plans/to-do/` |
| `notebook/`, `scratchpad/`, `thoughts/`, `notes/` | `plans/notes/` |
| `raw/`, `reference/` | `ref/` |
| `ingest/` | `ref/inbox/` |

## Plan Lifecycle

- Draft work in `plans/to-do/<slug>.md`.
- Move it to `plans/in-progress/<slug>.md` when work starts.
- Move it to `plans/completed/YYYY-MM-DD-<slug>.md` when complete.
- Keep non-status notes in `plans/notes/`.
- Update links when moving a plan; do not leave duplicate copies.

## Structure Markers

Create every canonical directory in greenfield and early-stage projects. Place and retain `.gitkeep` in each directory so the intended structure remains explicit and survives temporary emptiness.
