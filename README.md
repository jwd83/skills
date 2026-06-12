# [My Skills](https://github.com/jwd83/skills)

A personal collection of [agent skills](https://github.com/vercel-labs/skills) — reusable `SKILL.md` instruction sets for Claude Code, Codex, Cursor, and other coding agents.

## Install

List what's in this repo:

```bash
npx skills add jwd83/skills --list
```

Install everything:

```bash
npx skills add jwd83/skills
```

Install a specific skill:

```bash
npx skills add jwd83/skills --skill simplify
```

Install into a specific agent (e.g. Claude Code):

```bash
npx skills add jwd83/skills -a claude-code
```

## Manage

List what's currently installed:

```bash
npx skills list
```

Update installed skills to the latest versions:

```bash
npx skills update
```

Remove skills interactively, or target one by name:

```bash
npx skills remove
npx skills remove --skill simplify
```

Most commands accept `-g` for global (user-level) scope and `-a <agent>` to target a specific agent. Run `npx skills --help` for the full list.

## Skills

| Skill | What it does |
| --- | --- |
| [`architectural-review`](skills/architectural-review/SKILL.md) | Whole-project architecture review with metrics, ranked structural risks, and a behavior-preserving remediation plan |
| [`auto-research-repo`](skills/auto-research-repo/SKILL.md) | Create, audit, maintain, ingest into, query, or draft from cumulative research repositories with raw sources, a freeform notebook, wiki synthesis, manifests, wishlists, and portable HTML publication lanes |
| [`clumsy-ms-paint-redraw`](skills/clumsy-ms-paint-redraw/SKILL.md) | Redraw attached images as deliberately clumsy, scribbly MS Paint-style mouse drawings on white backgrounds |
| [`godot-gdscript-patterns`](skills/godot-gdscript-patterns/SKILL.md) | Godot 4 / GDScript patterns — signals, scenes, state machines, optimization |
| [`grill-me`](skills/grill-me/SKILL.md) | Stress-test a plan or design by interviewing you through every branch of the decision tree |
| [`local-wikipedia-search`](skills/local-wikipedia-search/SKILL.md) | Search and read Jared's publicly hosted text-only English Wikipedia Kiwix/ZIM mirror at `wiki.ayrscott.com` |
| [`next-step`](skills/next-step/SKILL.md) | Resume in-progress work, find the next defensible implementation step, make it, and sync docs/tests |
| [`pygame-patterns`](skills/pygame-patterns/SKILL.md) | Pygame-specific best practices and architecture for game loops, sprites, scenes/states, assets, input, collision, timing, rendering, packaging, and tests |
| [`python-refactor`](skills/python-refactor/SKILL.md) | Behavior-preserving Python refactoring with attention to PEP 8/257, typing, pytest, uv workflows, packaging, imports, resources, and idiomatic design |
| [`simplify`](skills/simplify/SKILL.md) | Review recently changed code and simplify it for clarity without changing behavior |
| [`system-verilog-expert`](skills/system-verilog-expert/SKILL.md) | SystemVerilog / RTL design guidance with synthesis, lint, CDC, and tool-flow-aware patterns |
| [`wiki-me`](skills/wiki-me/SKILL.md) | Build and maintain a persistent, interlinked markdown wiki from immutable sources plus a freeform notebook |

## Examples

Once installed, invoke a skill by its name or by describing what you want:

```
/simplify
```

```
/next-step
```

```
/python-refactor
```

```
/auto-research-repo
```

```
look this up in our local wiki
```

```
review this pygame game loop
```

```
grill me on this migration plan
```

```
start a wiki from these notes
```

```
Redraw the attached image in the most clumsy, scribbly, and utterly pathetic way possible. Use a white background, and make it look like it was drawn in MS Paint with a mouse
```

## Layout

```
skills/
  auto-research-repo/SKILL.md
  clumsy-ms-paint-redraw/SKILL.md
  godot-gdscript-patterns/SKILL.md
  grill-me/SKILL.md
  local-wikipedia-search/SKILL.md
  local-wikipedia-search/scripts/wiki-search.py
  local-wikipedia-search/scripts/wiki-article.py
  next-step/SKILL.md
  pygame-patterns/SKILL.md
  python-refactor/SKILL.md
  simplify/SKILL.md
  architectural-review/SKILL.md
  system-verilog-expert/SKILL.md
  wiki-me/SKILL.md
```

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name`, `description`) followed by the instructions the agent loads when triggered.
