---
name: architectural-review
description: Create and maintain a whole-project architectural review: a dated markdown assessment with objective metrics, preserved design strengths, ranked structural risks, and a concise behavior-preserving remediation plan. Use for architecture reviews, refactoring strategy, technical-debt assessment, or when resuming work from an existing architectural-review.md.
---

# Architectural Review

Use this skill for project-level architecture and refactoring assessments. The output is a durable `architectural-review.md` that both records the review and guides a short, behavior-preserving improvement campaign.

There are two modes:

- **Author the review** when no current `architectural-review.md` exists.
- **Execute the plan** when the document exists and the user asks to continue, start, or complete a numbered step.

Keep the review at the repository root unless the project already has a clear planning location such as `docs/`, `wiki/` or `plans/`.

## Mode 1: Author the review

### Establish the baseline

Review the repository before making judgments. Record the date, branch, and commit reviewed. Gather evidence such as:

- source, test, and documentation file counts and line counts;
- largest files/modules and their primary responsibilities;
- test command, pass/fail status, runtime, and coverage if available;
- dependency direction between major layers or packages;
- repeated implementations, duplicated workflows, or divergent conventions;
- project guidance (`README`, `CONTRIBUTING`, architecture docs, ADRs, existing plans) compared with the actual code.

Prefer measurable findings over impressions. If the project lacks a useful test baseline, call that out as a structural risk and make verification an early plan item.

### Write `architectural-review.md`

Use this structure:

```markdown
# Architectural Review — <Project>

*Reviewed <date> against `<branch>` @ `<short-hash>`.*

<One-paragraph executive summary: what is working, what is structurally expensive,
and the recommended order of attack. Mention related plan documents if they exist.>

## Snapshot
<Metrics table and brief interpretation. Include test baseline.>

## Structurally sound elements
<Load-bearing strengths to preserve. Explain why each matters.>

## Structural risks and costs
<Ranked findings, ordered by ongoing development cost. For each: evidence,
consequence, and a right-sized fix direction. End with “Smaller frictions” if useful.>

## Recommended order of attack
<5–8 numbered, behavior-preserving steps. Each step should be independently useful
and make later work cheaper.>

## Closing assessment
<Short final judgment: dominant risk, best leverage point, and expected payoff.>
```

### Review standards

- **Preserve what works.** The strengths section is a do-not-break list, not praise.
- **Rank by carrying cost.** Prioritize issues that tax routine development, testing, review, or release work.
- **Cite concrete evidence.** Use paths, approximate line numbers, counts, dependency examples, and test results.
- **Name present-day consequences.** Explain the current cost: fragile changes, slow verification, unclear ownership, circular dependencies, duplicated fixes, or difficult onboarding.
- **Avoid over-prescription.** Give a fix direction, not a detailed implementation spec.
- **Guard against overcorrection.** State when a finding does *not* require a heavier architecture, framework, or rewrite.
- **Keep the plan short.** An architectural review is not a backlog. Prefer 5–8 steps that can be completed across sessions.

Stop after delivering the review unless the user explicitly asks you to begin implementation.

## Mode 2: Execute the plan

### Before changing code

Re-establish the current state:

1. Read `architectural-review.md`, including all existing `*Done*` annotations.
2. Check the working tree and recent commits.
3. Re-read the files affected by the selected step.
4. Run or confirm the relevant test baseline.

If the repository has diverged from the review, adapt the step conservatively and record the discrepancy in the completion note.

### Implementation rules

- Work on one numbered step unless the user asks otherwise.
- Keep changes behavior-preserving unless the step explicitly authorizes behavior change.
- Prefer small, coherent commits with messages that reference the review step, e.g. `Step 3 architectural review: extract configuration loader`.
- Run the relevant tests after each coherent change; run the full suite when practical before finishing.
- Update documentation that the change directly invalidates.
- If an assumption in the review proves wrong, do not force the original plan. Adjust the implementation and document what changed.

### Mark the step complete

Annotate the completed item directly under its original numbered step. Do not rewrite the original analysis to make it appear more accurate in hindsight.

```markdown
3. **<Original step text.>**
   *Done <date>*, in <N> commit(s):
   - `<short-hash>`: <what changed, with useful counts or paths>.
   - `<short-hash>`: <additional part, if any>.

   Result: <tests run and outcome; important deviations; follow-ups deliberately left out of scope.>
```

The annotation should let a future session resume cold: what changed, what was verified, what surprised you, and what remains intentionally undone.

## Completing the campaign

When the final step is done, say so in its annotation. Do not extend the old review into an indefinite backlog. If more structural work is needed, create a new review against the new baseline.
