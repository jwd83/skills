---
name: project-layout
description: Project folder layout and organization best practices
---
What follows is general project layout guidance.

| Folder Path (assuming `./` is project root) | Folder Purpose | Alternative Path Examples |
| --- | --- | --- |
| `./docs` | A developer-facing source code manual for the project that documents design decisions and project standards and is viewable as simple HTML. | `./doc`, `./docs`, `./wiki`, `./docs/public`, `./docs/html` |
| `./plans` | Project plans and direction as HTML or Markdown files. | `./plan/` |
| `./plans/completed` | Completed plans for historical records. Finished plans move here, date-stamped with their completion date; for example: `2026-06-14-bug-report-4852.md`. |  |
| `./plans/in-progress` | In-progress work that will be useful for preserving active work between and within turns. |  |
| `./plans/notes` | Long-term project plans and guidance. |  |
| `./plans/to-do` | Tasks that are being drafted. Planning sessions append a journal to a file here. | `./plans/todos`, `./todos` |
| `./ref` | Immutable references and utilities that agents can reference and use but not modify. | `./reference`, `./raw` |

In a green field or early stage project a .gitkeep should be placed at each named folder location so we can establish a precedent for organization early in the project life cycle.
