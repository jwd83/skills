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

## Skills

| Skill | What it does |
| --- | --- |
| [`find-skills`](skills/find-skills/SKILL.md) | Discover and install skills from the open agent skills ecosystem when you ask "is there a skill for X?" |
| [`godot-gdscript-patterns`](skills/godot-gdscript-patterns/SKILL.md) | Godot 4 / GDScript patterns — signals, scenes, state machines, optimization |
| [`grill-me`](skills/grill-me/SKILL.md) | Stress-test a plan or design by interviewing you through every branch of the decision tree |
| [`simplify`](skills/simplify/SKILL.md) | Review recently changed code and simplify it for clarity without changing behavior |
| [`wiki-me`](skills/wiki-me/SKILL.md) | Build and maintain a persistent, interlinked markdown wiki from your sources |

## Examples

Once installed, invoke a skill by its name or by describing what you want:

```
/simplify
```

```
grill me on this migration plan
```

```
is there a skill for writing godot state machines?
```

```
start a wiki from these notes
```

## Layout

```
skills/
  find-skills/SKILL.md
  godot-gdscript-patterns/SKILL.md
  grill-me/SKILL.md
  simplify/SKILL.md
  wiki-me/SKILL.md
```

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name`, `description`) followed by the instructions the agent loads when triggered.
