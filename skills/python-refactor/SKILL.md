---
name: python-refactor
description: Standalone Python refactoring skill for behavior-preserving cleanup using Python best practices. Use when refactoring Python packages, scripts, CLIs, tests, async code, data models, or APIs with attention to PEP 8/257, typing, pytest, uv project/dependency management, packaging, imports, resource handling, and idiomatic Python design.
---

# Refactor Python

## Purpose

Refactor Python code safely and idiomatically while preserving behavior. Optimize for readable code, simple module boundaries, explicit contracts, useful tests, and maintainable Python. Avoid importing patterns from other ecosystems when simple functions, modules, dataclasses, protocols, or standard-library tools fit better.

Use this skill for cleanup, simplification, renaming, decomposition, dependency untangling, test characterization, typing improvements, packaging cleanup, or async/data-model refactors. Do **not** treat a rewrite, redesign, feature, or performance project as a refactor unless the user explicitly asks for that scope.

## Non-Negotiables

1. **Preserve behavior.** Keep public APIs, CLI flags, exceptions, log messages, file formats, ordering, database schemas, and side effects compatible unless the user approves a breaking change.
2. **Work from evidence.** Read code, tests, config, docs, and call sites before changing design.
3. **Make one coherent change at a time.** Prefer small, reviewable diffs over bundled redesigns.
4. **Protect risky behavior.** Run existing checks; add characterization tests when coverage is missing and the refactor is not trivial.
5. **Follow the project.** Match its Python version, formatter, linter, type checker, test style, package layout, and dependency manager.
6. **Avoid architecture astronautics.** Add abstractions only when duplication, volatility, or dependency direction justifies them.
7. **Do not hide behavior changes inside cleanup.** If you discover a bug, report it or fix it in a separate, explicit change.

## First Inspection Checklist

Before editing, identify:

- Tooling/config: `pyproject.toml`, `uv.lock`, `.python-version`, `setup.cfg`, `tox.ini`, `noxfile.py`, `pytest.ini`, `.pre-commit-config.yaml`, CI, or scripts.
- Working tree and recent changes: `git status`, `git diff`, and relevant recent tests when available.
- Supported Python versions from `requires-python`, lockfiles, CI, docs, or runtime constraints.
- Test/lint/type commands and whether the repo uses `pytest`, `unittest`, `tox`, `nox`, `ruff`, `black`, `isort`, `mypy`, `pyright`, `basedpyright`, or `pylint`.
- Public contracts: documented imports, `__init__.py`, `__all__`, entry points, CLIs, plugin hooks, serialized data, exceptions, and log output.
- Call sites before renaming, moving, or changing signatures.
- Dependency manager. If the project uses `uv`, use that workflow rather than manual virtualenv or `pip` commands.

## Safe Workflow

1. **Discover baseline.** Read relevant code/config and run a focused existing check if practical. Record pre-existing failures.
2. **Characterize when needed.** Add focused tests around current behavior before moving parsing, serialization, CLI behavior, async logic, or bug-prone code.
3. **Refactor one seam.** Rename, extract, inline, move, or simplify one coherent concept.
4. **Verify.** Run the narrowest useful tests/lint/type checks, expanding scope only as warranted.
5. **Review Python hazards.** Inspect the diff for accidental behavior changes; check imports/cycles, public contracts, mutable defaults, exception behavior, async cancellation, encodings, paths, timezone/money precision, and dependency metadata.
6. **Report clearly.** State files changed, checks run, compatibility notes, and remaining risk.

## Verification Commands

Use project-defined commands first. Common focused commands:

```bash
python -m pytest path/to/test_file.py -q
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m mypy package_or_module
python -m pyright
```

For `uv` projects, prefer the locked environment:

```bash
uv run pytest path/to/test_file.py -q
uv run ruff check .
uv run ruff format --check .
uv run mypy package_or_module
uv run pyright
uv sync --locked
uv lock --check
```

Do not run expensive full suites casually. If checks cannot run, explain what was inspected and what remains unverified.

## uv Projects

Treat a repo as uv-managed when you see `uv.lock`, `[tool.uv]`, `[tool.uv.workspace]`, or docs/scripts using `uv run`, `uv sync`, `uv add`, or `uv lock`.

- Run tools with `uv run <command>`.
- Add/remove dependencies with `uv add`, `uv add --dev`, and `uv remove`.
- Use `uv sync` to create/update the environment; use `uv sync --locked` or `uv lock --check` to verify without changing the lockfile.
- Do not hand-edit `uv.lock`.
- Do not introduce Poetry, Pipenv, `requirements.txt`, or manual `pip install` workflows into a uv project unless the repo already uses them for a specific purpose.
- Keep runtime dependencies in `project.dependencies` and dev-only tools in dependency groups.
- When removing imports, remove the corresponding dependency only after checking all code, extras, docs, and entry points.
- Preserve `requires-python`; do not add syntax or dependencies incompatible with it.

If uv is not already used, do not migrate to uv as part of a refactor unless asked.

## Refactoring Moves

Use the smallest move that clarifies the code:

- **Rename** confusing modules, functions, variables, types, or concepts after checking call sites.
- **Extract** cohesive functions/methods/modules from large blocks; pass only required data.
- **Inline** indirection that no longer earns its name.
- **Move** behavior closer to the data or dependency it primarily uses.
- **Separate pure logic from effects** so I/O, network, database, time, randomness, and environment access sit at boundaries.
- **Introduce dataclasses/enums/protocols/type aliases** only when they clarify invariants or stabilize a boundary.
- **Decompose conditionals** with guard clauses, named predicates, or dispatch when that is clearer and supported by the Python version.
- **Add compatibility re-exports** when moving public names that callers may import from old paths.

Example compatibility shim:

```python
# old_module.py
from .new_module import useful_function

__all__ = ["useful_function"]
```

## Smells and Preferred Responses

| Smell | Prefer | Avoid |
| --- | --- | --- |
| Long function | Extract named, cohesive steps | Splitting by arbitrary line count |
| Large class/module | Separate stable responsibilities | Many tiny anemic wrappers |
| Duplication | Extract the shared concept after confirming behavior matches | Abstracting coincidental similarity |
| Confusing names | Use domain terms from callers/tests/docs | Cute abbreviations or generic names |
| Long parameter list | Group cohesive values into a dataclass/config object | Giant untyped bags of unrelated data |
| Deep nesting | Guard clauses and named predicates | Clever control flow that hides branches |
| Primitive obsession | `Enum`, `Literal`, `NewType`, `TypedDict`, or dataclasses when they enforce meaning | Heavy classes for every scalar |
| Hidden side effects | Make dependencies explicit at boundaries | Helpers that look pure but perform I/O |
| Circular imports | Move shared types/helpers lower; use `if TYPE_CHECKING:` | Import-time hacks or monkeypatching |
| Dead private code | Remove it and any tests that only covered it | Deleting public behavior tests or leaving commented alternatives |

## Python-Specific Guidance

### Data and state

- Use mutable defaults safely: `None` sentinels or `dataclasses.field(default_factory=...)`.
- Prefer dataclasses, `NamedTuple`, `TypedDict`, or existing models for dict-shaped structured data; choose based on mutability and boundary needs.
- Use `slots=True` only when supported and safe for public classes; it can affect dynamic attributes, inheritance, and pickling.
- Avoid boilerplate getter/setter classes. Use plain attributes or properties with real invariants.
- Prefer composition, functions, or `typing.Protocol` over deep inheritance unless runtime registration or shared implementation is needed.

### Imports, modules, and packaging

- Avoid import-time side effects: expensive I/O, network calls, logging configuration, environment mutation, argument parsing, or display/database initialization.
- Move script bodies behind `main()` and return exit codes:

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

- Preserve documented import paths, entry points, and `__all__`.
- Keep CLI/framework adapters and infrastructure separate from domain logic where practical.

### Resources and external effects

- Use context managers for files, locks, temporary directories, database sessions, and network clients.
- Prefer `pathlib.Path` for new internal path handling unless project style or APIs favor strings.
- Specify encodings for text files when behavior should be stable.
- Make time, randomness, clients, repositories, and configuration explicit dependencies when that improves testability.

### Exceptions and errors

- Preserve public exception types/messages during refactors.
- Avoid bare `except:` and broad `except Exception` unless intentionally isolating a boundary.
- Chain exceptions when translating errors: `raise DomainError(...) from exc`.
- Do not swallow `asyncio.CancelledError`; preserve cancellation behavior.

### Typing

Add or improve types when they clarify contracts and the project supports typing.

- Prefer built-in generics (`list[str]`) when supported and `collections.abc` interfaces (`Iterable`, `Sequence`, `Mapping`, `Callable`) for accepted inputs.
- Use `Protocol` for structural boundaries, `TypeAlias` for repeated complex types, and `object` instead of `Any` when callers must narrow.
- Use `Self`, `override`, `assert_never`, `match`, `StrEnum`, or `datetime.UTC` only when the configured Python/type-checker version supports them, or when the project already uses compatible backports.
- Avoid lying annotations, invasive typing rewrites, unnecessary `cast()`, and weakening typed code with `Any`.
- Separate runtime imports from type-only imports with `if TYPE_CHECKING:` when needed to avoid cycles.

### Async, precision, and performance-sensitive behavior

- Preserve sync/async public contracts.
- Do not call blocking I/O directly inside async functions; use async libraries or executors.
- Keep event loop creation at application boundaries.
- Use timezone-aware datetimes for real-world timestamps.
- Use `Decimal` for money/exact decimal calculations; do not replace it with `float` during cleanup.
- Do not optimize blindly. Measure first if performance is the goal or a hot path is being changed.

## Testing Guidance

- Prefer focused tests that lock current behavior before changing internals.
- Use `pytest` fixtures/parametrization, `tmp_path`, `monkeypatch`, `capsys`, and `caplog` when they fit.
- Use mocks sparingly; assert externally visible behavior rather than implementation details.
- Keep tests deterministic by controlling time, randomness, locale, filesystem, and network.
- Consider property tests for parsers, serializers, validators, and numeric invariants when already in use or clearly valuable.

## Anti-Patterns to Avoid

- Refactoring by formatting the whole repository unless requested.
- Mixing unrelated cleanup with feature work or bug fixes.
- Adding design patterns because a conditional exists.
- Turning every function into a class or every scalar into a value object.
- Replacing readable loops with dense comprehensions.
- Introducing optional dependencies for small standard-library tasks.
- Moving code without checking imports, entry points, docs, and compatibility exports.
- Changing public exception/log/message/data behavior casually.
- Hiding mutable configuration in module globals.

## Final Response Checklist

When reporting back, include:

- What refactoring was done and why.
- Files changed.
- Tests/checks run and outcomes.
- Compatibility notes for moved or public APIs.
- Follow-up work that should remain separate.
