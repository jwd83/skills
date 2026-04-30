---
name: refactor
description: Surgical, language-agnostic code refactoring to improve maintainability without changing behavior. Use when cleaning up existing code, reducing duplication, clarifying boundaries, improving naming, decomposing large functions/classes/modules, or making incremental design improvements. Prefer a language-specific skill when one exists.
license: MIT
---

# Refactor

## Purpose

Improve internal code structure while preserving externally observable behavior. Treat refactoring as controlled evolution: understand first, protect behavior with tests or characterization checks, make the smallest safe change, verify, then repeat.

This skill is intentionally language-agnostic. When a task is clearly language-specific, also load the relevant language skill if available, such as `refactor-python` for Python code.

## When to Use

Use this skill when the user asks to:

- Refactor, clean up, simplify, reorganize, or improve maintainability.
- Reduce duplication or coupling.
- Rename confusing functions, variables, modules, types, or concepts.
- Break down large functions, classes, modules, components, or services.
- Improve boundaries between layers or responsibilities.
- Add tests around existing behavior before changing internals.

Do **not** use it for a rewrite, redesign, performance project, or feature addition unless the user explicitly wants refactoring as a step toward that goal.

## Non-Negotiables

1. **Preserve behavior.** Do not mix refactoring with feature changes unless explicitly asked.
2. **Work from evidence.** Read the code, tests, config, and call sites before changing design.
3. **Prefer small steps.** Make one coherent refactoring at a time.
4. **Protect behavior.** Run existing tests; add characterization tests when risk is high and tests are missing.
5. **Keep public contracts stable.** APIs, data formats, CLI flags, database schemas, errors, and side effects must remain compatible unless the user approves a breaking change.
6. **Use the project's style.** Follow existing conventions before introducing new patterns.
7. **Avoid architecture astronautics.** Do not add abstractions until duplication, volatility, or dependency direction justifies them.

## Standard Workflow

### 1. Inspect

- Identify the language, framework, package layout, and test tooling.
- Read the target code and its direct callers/callees.
- Check recent changes if available (`git diff`, `git status`, relevant tests).
- Find the smallest behavior-preserving improvement.

### 2. Characterize

- Run focused tests first, then broader tests if practical.
- If no tests exist, add minimal characterization tests or document manual checks.
- Capture expected behavior before editing risky logic.

### 3. Plan a Small Move

Choose one refactoring operation:

- Rename for clarity.
- Extract function/method/module/class.
- Inline unnecessary indirection.
- Move code to the owner of the concept.
- Replace duplicated logic with a shared helper.
- Split mixed responsibilities.
- Replace conditionals with a table, strategy, polymorphism, or data-driven dispatch only when simpler.
- Introduce a value object/type only when it protects a meaningful domain invariant.

### 4. Edit

- Keep diffs focused and reviewable.
- Preserve import/export behavior and public names unless intentionally migrated with compatibility aliases.
- Avoid formatting unrelated code unless the project's formatter does it.
- Do not silently change error handling, ordering, precision, concurrency, I/O, logging, or performance characteristics.

### 5. Verify

- Run the most relevant tests/linters/type checks available.
- Inspect the diff for accidental behavior changes.
- If tests cannot run, explain why and list manual verification performed.

## Code Smells and Refactoring Responses

| Smell | Prefer | Avoid |
| --- | --- | --- |
| Long function | Extract cohesive steps with names that reveal intent | Splitting by arbitrary line count |
| Large class/module | Separate responsibilities around stable concepts | Creating many tiny anemic wrappers |
| Duplication | Extract the shared concept after confirming behavior is truly the same | Abstracting coincidental similarity |
| Confusing names | Rename to domain terms used by callers/tests/docs | Cute abbreviations or generic names |
| Long parameter list | Group cohesive parameters into an existing domain object or small parameter object | Passing giant bags of unrelated data |
| Deep nesting | Guard clauses, decomposed predicates, clearer validation flow | Obscuring control flow with clever constructs |
| Primitive obsession | Value objects, enums, tagged unions, validated types where supported | Heavy classes for every scalar |
| Feature envy | Move behavior closer to the data or expose an intention-revealing method | Reaching through object internals |
| Shotgun surgery | Centralize volatile decisions behind one module/function/type | Global registries or hidden magic |
| Dead code | Remove unused code and tests; trust version control | Leaving commented-out alternatives |
| Hidden side effects | Make side effects explicit at boundaries | Pretending impure code is pure |
| Circular dependencies | Extract shared abstractions or invert dependencies | Import hacks or runtime monkeypatching |

## Refactoring Operations

Use the smallest operation that solves the problem:

- **Rename:** improve intent without changing behavior.
- **Extract function/method:** isolate a coherent operation and pass only required data.
- **Inline function/method:** remove indirection that no longer clarifies.
- **Extract module/package:** separate unrelated responsibilities and stabilize imports.
- **Move function/method:** put behavior with the data or dependency it primarily uses.
- **Extract interface/protocol/abstraction:** introduce only at a real boundary or variation point.
- **Introduce parameter object:** group fields that travel together and have one meaning.
- **Replace conditional with dispatch:** use maps, strategies, polymorphism, or pattern matching when it reduces complexity.
- **Decompose conditional:** name complex predicates and isolate branches.
- **Replace magic literal with named constant:** clarify units and domain meaning.
- **Encapsulate collection/state:** protect invariants while keeping simple access simple.
- **Separate pure logic from effects:** make core behavior easier to test.

## Testing Guidance

Before and after refactoring, choose the narrowest useful checks:

- Unit tests for pure logic.
- Integration tests for boundary behavior.
- Snapshot/golden/characterization tests for legacy behavior.
- Contract tests for public APIs and adapters.
- Property tests for invariants when applicable.
- Type checks, linters, formatters, or build commands already used by the project.

If tests are absent and adding them is too large, make a smaller refactor or ask for confirmation before proceeding.

## Safety Checklist

Before editing:

- [ ] I know the public behavior and call sites.
- [ ] I know how to run at least one relevant verification command.
- [ ] I have identified one small refactoring, not a bundle of unrelated changes.

After editing:

- [ ] Public APIs and data formats are unchanged or compatibility is preserved.
- [ ] Tests/checks were run, or limitations are clearly stated.
- [ ] Names and boundaries are clearer.
- [ ] Complexity moved down, not sideways.
- [ ] No unrelated formatting or feature work was introduced.

## Output Style

When reporting back to the user:

- State the specific refactoring performed.
- List changed files.
- Mention verification commands and results.
- Call out any behavior-preservation assumptions or follow-up risks.
