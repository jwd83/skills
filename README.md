# [My Skills](https://github.com/jwd83/skills)

A personal collection of [agent skills](https://github.com/vercel-labs/skills) — reusable `SKILL.md` instruction sets for Claude Code, Codex, Cursor, and other coding agents.

## Install

```bash
npx skills add jwd83/skills --list
npx skills add jwd83/skills
npx skills add jwd83/skills --skill simplify
npx skills add jwd83/skills -a claude-code
```

Use `--list` to inspect what's available, omit it to install everything, pass `--skill <name>` for one skill, and add `-a <agent>` to target a specific agent.

## Manage

```bash
npx skills list
npx skills update
npx skills remove
npx skills remove --skill simplify
```

Most commands accept `-g` for global (user-level) scope and `-a <agent>` to target a specific agent. Run `npx skills --help` for the full list.

## Notes

Skills live under `skills/<name>/SKILL.md`. Once installed, invoke one by name (`/simplify`) or by describing the task (`grill me on this migration plan`).

Each skill directory contains a `SKILL.md` with YAML frontmatter (`name`, `description`) followed by the instructions the agent loads when triggered.
