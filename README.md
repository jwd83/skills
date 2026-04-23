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
| [`godot-gdscript-patterns`](skills/godot-gdscript-patterns/SKILL.md) | Godot 4 / GDScript patterns — signals, scenes, state machines, optimization |
| [`grill-me`](skills/grill-me/SKILL.md) | Stress-test a plan or design by interviewing you through every branch of the decision tree |
| [`next-step`](skills/next-step/SKILL.md) | Resume in-progress work, find the next defensible implementation step, make it, and sync docs/tests |
| [`simplify`](skills/simplify/SKILL.md) | Review recently changed code and simplify it for clarity without changing behavior |
| [`system-verilog-expert`](skills/system-verilog-expert/SKILL.md) | SystemVerilog / RTL design guidance with synthesis, lint, CDC, and tool-flow-aware patterns |
| [`wiki-me`](skills/wiki-me/SKILL.md) | Build and maintain a persistent, interlinked markdown wiki from your sources |

## Examples

Once installed, invoke a skill by its name or by describing what you want:

```
/simplify
```

```
/next-step
```

```
grill me on this migration plan
```

```
start a wiki from these notes
```

## Layout

```
skills/
  godot-gdscript-patterns/SKILL.md
  grill-me/SKILL.md
  next-step/SKILL.md
  simplify/SKILL.md
  system-verilog-expert/SKILL.md
  wiki-me/SKILL.md
```

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name`, `description`) followed by the instructions the agent loads when triggered.
