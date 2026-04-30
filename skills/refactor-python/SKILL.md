---
name: refactor-python
description: Python-specific refactoring skill for behavior-preserving cleanup using Python best practices. Use when refactoring Python packages, scripts, CLIs, tests, async code, data models, or APIs with attention to PEP 8/257, typing, pytest, uv project/dependency management, packaging, imports, resource handling, and idiomatic Python design.
license: MIT
---

# Refactor Python

## Purpose

Refactor Python code safely and idiomatically while preserving behavior. Optimize for readability, simple module boundaries, explicit contracts, good tests, and maintainable Python—not for translating patterns from JavaScript, Java, or enterprise OO into Python.

Use this skill together with the general `refactor` skill when the user asks to clean up or restructure Python code.

## Python Refactoring Principles

1. **Behavior first.** Keep public APIs, CLI behavior, exceptions, logs, return values, file formats, database queries, and side effects stable unless the user approves a change.
2. **Prefer simple Python.** Clear functions, modules, dataclasses, protocols, and standard library tools usually beat heavy design patterns.
3. **Respect project conventions.** Follow the repository's existing formatter, linter, type checker, test style, and package layout.
4. **Make illegal states harder.** Use type hints, enums, dataclasses, validation at boundaries, and narrow interfaces where they clarify invariants.
5. **Separate pure logic from effects.** Keep I/O, network, database, time, randomness, and environment access at boundaries so core logic is easy to test.
6. **Avoid cleverness.** Readability is more important than dense comprehensions, metaprogramming, decorators, or dynamic imports.
7. **Refactor incrementally.** One coherent change, then run focused checks.

## First Inspection Checklist

Before changing Python code, inspect:

- `pyproject.toml`, `uv.lock`, `.python-version`, `setup.cfg`, `tox.ini`, `noxfile.py`, `pytest.ini`, `.pre-commit-config.yaml`, or equivalent tooling.
- Project manager: prefer existing workflow; if the project uses `uv`, use `uv run`, `uv add`, `uv remove`, `uv sync`, and `uv lock` instead of manually editing environments.
- Test framework and commands: usually `pytest`, sometimes `unittest`, `tox`, `nox`, or framework-specific commands.
- Formatter/linter/type checker: commonly `ruff`, `black`, `isort`, `mypy`, `pyright`, `basedpyright`, `pylint`.
- Supported Python versions from `requires-python`, `.python-version`, CI, or lockfiles; do not introduce syntax or typing features unsupported by the project.
- Public package exports: `__init__.py`, documented imports, entry points, CLIs, plugin hooks.
- Call sites before renaming or moving symbols.

## Verification Commands

Use project-defined commands first. If absent, common focused commands are:

```bash
python -m pytest path/to/test_file.py -q
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m mypy package_or_module
python -m pyright

# If the project uses uv, prefer the locked environment:
uv run pytest path/to/test_file.py -q
uv run ruff check .
uv run mypy package_or_module
uv run pyright
uv sync --locked
```

Do not run expensive full suites without considering scope. If checks are unavailable, explain what was inspected and what remains unverified.

## uv Project and Dependency Management

If a Python project uses `uv`, preserve and use that workflow.

### Detect uv usage

Treat the project as uv-managed when you see any of:

- `uv.lock`
- `[tool.uv]` in `pyproject.toml`
- Documentation or scripts using `uv run`, `uv sync`, `uv add`, or `uv lock`
- A workspace layout under `[tool.uv.workspace]`

### Refactoring rules for uv projects

- Use `uv run <command>` for tests, linters, scripts, and CLIs so checks run in the project's resolved environment.
- Use `uv add <package>` for runtime dependencies and `uv add --dev <package>` for development dependencies.
- Use `uv remove <package>` when deleting a dependency.
- Use `uv sync` to create/update the environment from `pyproject.toml` and `uv.lock`.
- Use `uv sync --locked` or `uv lock --check` in verification when you must ensure the lockfile is current without changing it.
- Do not hand-edit `uv.lock`.
- Do not mix package managers casually. Avoid introducing `requirements.txt`, Poetry, Pipenv, or manual `pip install` workflows into a uv project unless the repository already uses them for a specific purpose.
- Keep dependency groups intentional: runtime dependencies in `project.dependencies`; developer-only tools in dependency groups such as `dev`.
- When removing imports during refactors, check whether the corresponding dependency can also be removed; only remove it if no other code, extras, docs, or entry points need it.
- Preserve `requires-python`; do not add dependencies or syntax incompatible with the declared Python versions.

### Useful uv commands

```bash
uv sync
uv sync --locked
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv add requests
uv add --dev pytest ruff mypy
uv remove requests
uv lock --check
```

If uv is not already used, do not migrate the project to uv as part of a refactor unless the user explicitly asks.

## Python Smells and Preferred Refactorings

### Large functions that mix policy and effects

Prefer extracting pure helpers and passing dependencies in explicitly.

```python
# Better shape
def build_invoice(order: Order, rates: Rates) -> Invoice:
    ...  # pure calculation


def send_invoice(order_id: str, repo: OrderRepository, mailer: Mailer) -> None:
    order = repo.get(order_id)
    invoice = build_invoice(order, repo.current_rates())
    mailer.send(invoice)
```

Avoid hiding I/O in helpers named like pure calculations.

### Mutable default arguments

Replace mutable defaults with `None` sentinels or `default_factory`.

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

For dataclasses:

```python
from dataclasses import dataclass, field

@dataclass
class User:
    tags: list[str] = field(default_factory=list)
```

### Primitive obsession

Use lightweight domain types when they enforce meaning.

- `Enum`/`StrEnum` for closed sets.
- `dataclass(frozen=True)` for small value objects.
- `NewType` for static distinction with no runtime overhead.
- `Literal` for narrow public options.
- `TypedDict` for dict-shaped external data.
- Pydantic/attrs only when already used by the project or needed at validation boundaries.

Avoid building Java-style getter/setter classes around simple data.

### Dicts carrying structured data everywhere

Prefer a dataclass, `NamedTuple`, `TypedDict`, or existing model depending on mutability and boundary needs.

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str
```

Use `slots=True` only when supported and beneficial; avoid changing pickling/attribute behavior for public classes without care.

### Long parameter lists

Group cohesive values into dataclasses/config objects, but avoid untyped catch-all config bags.

```python
@dataclass(frozen=True)
class RetryPolicy:
    attempts: int
    timeout_seconds: float
    backoff_seconds: float
```

### Deep nesting and complex conditionals

Use guard clauses, named predicates, or `match` only when clearer and supported by the Python version.

```python
def process(user: User | None) -> Result:
    if user is None:
        return Result.error("missing user")
    if not user.is_active:
        return Result.error("inactive user")
    return process_active_user(user)
```

### Broad exceptions and swallowed errors

Avoid bare `except:` and broad `except Exception` unless intentionally isolating a boundary. Preserve exception behavior during refactors.

```python
try:
    payload = json.loads(raw)
except json.JSONDecodeError as exc:
    raise InvalidPayloadError("invalid JSON") from exc
```

### Resource management

Use context managers for files, locks, temporary directories, database sessions, and network clients.

```python
from pathlib import Path

with Path(path).open(encoding="utf-8") as file:
    data = file.read()
```

Prefer `pathlib.Path` for new internal path manipulation unless the project consistently uses strings or APIs require strings.

### Import-time side effects

Do not perform expensive I/O, network calls, logging configuration, environment mutation, or argument parsing at import time. Move script behavior under:

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### Global state and hidden dependencies

Prefer explicit dependency injection for time, randomness, clients, repos, and configuration. Use module constants for true constants only.

### Inheritance-heavy designs

Prefer composition, simple functions, or `typing.Protocol` over deep inheritance when behavior varies.

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, message: str) -> None: ...
```

Use abstract base classes when runtime registration or shared implementation is genuinely needed.

### Overuse of classes

If a class has no state or invariant, a module-level function may be clearer. If a module has many functions manipulating the same state shape, a dataclass or class may be appropriate.

### Boolean flags controlling many branches

Split into clearer functions or use strategies. Preserve the public API by keeping the flag wrapper if needed.

```python
def render_text(report: Report) -> str: ...
def render_html(report: Report) -> str: ...
```

### Large comprehensions

Use comprehensions for simple transformations. Extract loops when filtering, transformation, side effects, or error handling become hard to read.

### Time, money, and precision

- Use timezone-aware datetimes for real-world timestamps.
- Prefer `datetime.UTC` where supported; otherwise use `datetime.timezone.utc`.
- Use `Decimal` for money and exact decimal calculations.
- Do not replace `Decimal` with `float` during cleanup.

### Async code

- Preserve sync/async public contracts.
- Do not call blocking I/O directly inside async functions; use async libraries or executors.
- Use `asyncio.TaskGroup` only when supported by the Python version.
- Preserve cancellation behavior; do not swallow `asyncio.CancelledError`.
- Keep event loop creation at application boundaries.

## Typing Guidance

Add or improve type hints when they clarify contracts and the project supports typing.

Prefer:

- Built-in generics: `list[str]`, `dict[str, int]` when supported.
- `collections.abc` for accepted interfaces: `Iterable`, `Sequence`, `Mapping`, `Callable`.
- `Protocol` for structural interfaces at boundaries.
- `TypeAlias` for complex repeated types.
- `Self`, `override`, `assert_never` only when supported by the configured Python/type-checker version.
- `object` instead of `Any` when callers must narrow.

Be careful:

- Do not add types that lie or require invasive rewrites.
- Avoid `cast()` unless the invariant is documented nearby.
- Avoid weakening typed code with `Any`.
- If using `from __future__ import annotations`, match project style and Python version needs.
- Keep runtime imports and type-only imports separate with `if TYPE_CHECKING:` when needed to avoid cycles.

## Module and Package Boundaries

When moving Python code:

- Preserve documented imports and public names.
- Update `__all__` if the project uses it.
- Avoid creating circular imports; move shared types/helpers to lower-level modules only when justified.
- Keep CLI, framework adapters, and infrastructure separate from domain logic where practical.
- Use compatibility re-exports for moved public APIs when callers may depend on old paths.

Example compatibility shim:

```python
# old_module.py
from .new_module import useful_function

__all__ = ["useful_function"]
```

## Testing Guidance for Python Refactors

Prefer focused tests that lock current behavior before changing internals.

- Use `pytest` fixtures and parametrization for repeated cases.
- Use `tmp_path` for filesystem tests.
- Use `monkeypatch` for environment variables and targeted dependency replacement.
- Use `capsys`/`caplog` for stdout/stderr/logging behavior.
- Use `unittest.mock` sparingly and assert behavior, not implementation details.
- Consider Hypothesis/property tests for parsers, serializers, validators, and numeric invariants if already in use or appropriate.
- Keep tests deterministic: control time, randomness, locale, filesystem, and network.

For legacy code without tests, add characterization tests around public behavior before extraction or movement.

## Tooling and Style

Follow the repository's tools. In uv-managed projects, run tools through `uv run` and modify dependencies with `uv add`/`uv remove` rather than ad hoc virtualenv or pip commands. If choosing defaults for a small unconfigured project:

- Format with `ruff format` or `black`, not both unless configured.
- Lint with `ruff check`.
- Type-check with `mypy` or `pyright` if the project already uses one.
- Keep imports sorted according to the configured tool.
- Follow PEP 8 naming: `snake_case` functions/variables, `PascalCase` classes, `UPPER_CASE` constants.
- Use PEP 257 docstrings for public modules/classes/functions when docs add value; do not restate obvious code.

## Common Python Refactoring Moves

- Extract pure function from method or script.
- Move script body into `main()` and return an exit code.
- Replace ad hoc tuples/dicts with dataclasses or typed dicts.
- Replace string status codes with enums where the domain is closed.
- Replace repeated path string operations with `pathlib.Path`.
- Replace manual open/close with context managers.
- Replace duplicated validation with a named validator function or model boundary.
- Replace deep mocks with dependency injection and lightweight fakes.
- Replace inheritance with composition or protocols.
- Split framework adapters from domain services.
- Add compatibility re-export after moving a public function/class.
- Narrow overly broad exception handling.
- Introduce constants for units, limits, and domain values.

## Anti-Patterns to Avoid

- Importing JavaScript/TypeScript habits into Python: builder chains for simple objects, interface-per-class designs, Promise-like abstractions, or excessive callbacks.
- Adding design patterns just because a conditional exists.
- Turning every function into a class.
- Adding getters/setters that do nothing; use attributes/properties idiomatically.
- Using mutable module globals for hidden configuration.
- Refactoring by formatting the whole repository unless requested.
- Changing public exception types/messages casually; tests and users may depend on them.
- Replacing simple readable loops with dense comprehensions.
- Introducing optional dependencies for small standard-library tasks.
- Moving code without checking imports, entry points, docs, and `__all__`.

## Safe Python Refactoring Workflow

1. **Discover tooling and Python version.** Read config, including `pyproject.toml`, `uv.lock`, and `.python-version` when present, before writing syntax.
2. **Run focused baseline checks.** Record failing tests before editing.
3. **Add characterization coverage if needed.** Especially for parsing, serialization, CLI, or bug-prone logic.
4. **Make one refactoring.** Keep public behavior stable.
5. **Run focused tests/lint/type checks.** Expand only as warranted.
6. **Review diff for Python-specific hazards:** imports, cycles, mutable defaults, exception behavior, async cancellation, encoding, path handling, timezone/Decimal precision.
7. **Report clearly.** Mention files changed, checks run, and any remaining risk.

## Final Response Checklist

When reporting to the user, include:

- What Python-specific issue was addressed.
- Files changed.
- Tests/checks run and outcomes.
- Any compatibility shims or public API preservation notes.
- Any follow-up that should be done separately.
