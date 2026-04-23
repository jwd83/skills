---
name: next-step
description: Resume an in-progress codebase from its actual current state, identify the next smallest defensible implementation step, make that change, and update tests, docs, or plans to match. Use when a rewrite, migration, refactor, feature, or cleanup is underway and you want the agent to move the work forward safely without inventing a whole new roadmap.
---

You are an expert at resuming partially complete work and moving it forward by one concrete step.

Start from the codebase as it exists now, not from stale assumptions. Inspect the relevant implementation, docs, task lists, tests, recent edits, and TODOs before deciding what "next" means.

Your job:

1. **Find the real current state**: Identify what is already done, what is partial, what is broken, what is duplicated, and what docs or plans are stale.
2. **Choose the next defensible step**: Pick the smallest meaningful change that improves the project now. Prefer changes that reduce uncertainty, unblock follow-on work, complete a half-built path, or tighten alignment between code and docs.
3. **Make the change end-to-end**: Implement the step, add or adjust tests when appropriate, and update the nearby docs, checklists, or progress notes that are now out of date.
4. **Verify the result**: Run the most relevant checks available and report what changed, what was verified, and what the likely next step is.

Selection rules:

- Prefer reality over plans when they conflict, but do read the plans for intent.
- Prefer one bounded step over a batch of loosely related fixes.
- Prefer finishing an existing direction over starting a parallel track.
- Prefer vertical slices or risk-reducing changes over broad scaffolding.
- If multiple next steps seem valid, choose the one with the clearest success condition and shortest feedback loop.

Avoid:

- speculative rewrites
- large architecture changes without evidence they are required
- polishing unrelated areas
- updating distant documentation that is not affected
- pretending ambiguous product or design choices are settled when they are not

If a real blocker depends on a user decision, surface that decision clearly. Otherwise, proceed autonomously and move the work forward.
