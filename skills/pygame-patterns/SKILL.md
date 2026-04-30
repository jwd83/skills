---
name: pygame-patterns
description: Pygame-specific best practices, architecture patterns, and antipatterns for Python games. Use when building, refactoring, debugging, or reviewing pygame projects, including game loops, sprites, scenes/states, assets, input, collision, timing, rendering, packaging, and tests.
license: MIT
---

# Pygame Patterns

## Purpose

Build and refactor pygame projects using idiomatic Python and pygame-specific practices. Use this skill with `refactor-python` when cleaning up pygame code.

Optimize for a stable game loop, clear separation of update/draw/input concerns, predictable timing, efficient asset handling, and simple architecture that fits the game's size.

## First Inspection Checklist

Before editing a pygame project, inspect:

- Python/project tooling: `pyproject.toml`, `uv.lock`, `.python-version`, test config, run scripts.
- Entry point: where `pygame.init()`, `display.set_mode()`, and the main loop are called.
- Game loop: event handling, update timing, drawing, `display.flip()`/`update()`, and `Clock.tick()`.
- Asset loading: image, sound, font, map, and data paths.
- State management: menu, gameplay, pause, game over, settings.
- Sprite/entity organization: `pygame.sprite.Sprite`, groups, rects, masks, custom entities.
- Input model: event-based actions vs held-key state.
- Collision code and coordinate system.
- Tests or headless support.

If the project uses `uv`, prefer commands such as:

```bash
uv run python -m your_game
uv run pytest -q
uv run ruff check .
uv add pygame
```

Do not migrate a non-uv project to uv unless the user asks.

## Core Architecture Pattern

For small and medium pygame games, prefer a simple `Game` application object plus scenes/states.

```python
class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene: Scene = TitleScene(self)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.scene.handle_events(events)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
```

Keep `pygame.init()` and the display setup at the application boundary, not at import time.

## Main Loop Best Practices

- Pump events every frame with `pygame.event.get()` or equivalent; otherwise the OS may mark the window unresponsive.
- Use `pygame.time.Clock().tick(fps)` to cap frame rate and compute delta time.
- Use `dt` for movement and timers where frame-rate independence matters.
- Keep the loop order consistent: collect events, handle input, update simulation, draw, flip/update display.
- Draw the entire frame each loop unless deliberately optimizing dirty rectangles.
- Use `pygame.display.flip()` for full-screen redraws; use `pygame.display.update(rects)` only when intentionally tracking dirty regions.
- Keep shutdown explicit: exit loop, clean up, call `pygame.quit()`, return an exit code from `main()`.

## Input Patterns

Use events for one-shot actions:

- quit
- pause toggle
- menu selection
- jump pressed
- button clicked

Use held-key state for continuous actions:

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player.velocity.x = -PLAYER_SPEED
```

Avoid scattering direct keyboard checks across many unrelated objects. Prefer a small input layer or pass actions to objects that need them.

## Scene and State Patterns

Use explicit scenes/states for major modes:

- `TitleScene`
- `GameScene`
- `PauseScene`
- `GameOverScene`
- `SettingsScene`

A scene typically owns its sprites, UI elements, and transition decisions:

```python
class Scene:
    def handle_events(self, events: list[pygame.event.Event]) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
```

Avoid one giant `while running` loop with hundreds of branches for every menu and game mode.

## Sprite and Entity Patterns

Use `pygame.sprite.Sprite` and groups when they simplify update/draw/collision.

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.position = pygame.Vector2(self.rect.center)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rect.center = round(self.position.x), round(self.position.y)
```

Guidelines:

- Keep float positions separately from integer `Rect`s for smooth movement.
- Use `pygame.Vector2` for velocity, acceleration, and direction math.
- Use groups for batch `update()`, `draw()`, and collisions.
- Keep entity update logic focused; move spawning, level loading, and global orchestration to scene/system code.
- Prefer composition for behaviors when inheritance gets deep.

## Rendering and Asset Handling

Load assets once, then reuse them.

- Load images during scene/resource initialization, not inside `draw()` or per-frame `update()`.
- Call `.convert()` or `.convert_alpha()` after display initialization for faster blitting.
- Cache fonts and rendered static text where practical.
- Use sprite sheets or atlases when appropriate, but keep tooling simple.
- Centralize asset paths with `pathlib.Path` or `importlib.resources` for packaged games.
- Preserve alpha needs: use `convert_alpha()` for transparent sprites, `convert()` for opaque backgrounds.

Example resource helper:

```python
ASSET_DIR = Path(__file__).resolve().parent / "assets"


def load_image(name: str, *, alpha: bool = True) -> pygame.Surface:
    image = pygame.image.load(ASSET_DIR / name)
    return image.convert_alpha() if alpha else image.convert()
```

## Timing, Physics, and Movement

- Use seconds for `dt` (`milliseconds / 1000.0`) and document units.
- Use constants for speeds, gravity, friction, cooldowns, and tile sizes.
- For arcade games, variable timestep with capped FPS is often enough.
- For deterministic physics, consider a fixed-step simulation accumulator, but only when needed.
- Clamp extreme `dt` values after stalls or debugging pauses to prevent tunneling or huge jumps.
- Keep collision resolution deterministic and simple before adding complex physics.

## Collision Patterns

Choose the cheapest collision that fits:

- `Rect` collision for most arcade/tile games.
- Circle/radius checks for approximate radial collision.
- `pygame.mask` pixel-perfect collision only when necessary; masks are more expensive.
- Tilemap spatial partitioning for many static colliders.
- Broad-phase filtering before expensive checks.

Keep collision detection separate from collision response when it improves clarity.

## Audio Practices

- Initialize mixer deliberately if custom frequency/buffer settings matter.
- Load sound effects once and reuse `pygame.mixer.Sound` objects.
- Use channels for overlapping sounds when needed.
- Keep music streaming separate from short sound effects.
- Avoid blocking loads during gameplay.

## UI and Text

- Cache static rendered text surfaces.
- Re-render dynamic text only when the value changes, not every frame unnecessarily.
- Keep UI layout code separate from gameplay simulation.
- Use `Rect` alignment helpers (`center`, `midtop`, `topleft`) for readable positioning.

## Testing Pygame Code

Make core game logic testable without opening a window:

- Extract pure logic for scoring, movement rules, cooldowns, state transitions, inventory, AI decisions, and level parsing.
- Keep pygame display and audio initialization at boundaries.
- For tests that import pygame modules in CI/headless environments, set dummy drivers before initialization when needed:

```python
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
```

- Use `pytest` for pure logic tests.
- Avoid brittle tests that depend on exact frame timing unless timing is the behavior under test.

## Packaging and Project Layout

Prefer a package layout that keeps game code importable:

```text
project/
├── pyproject.toml
├── uv.lock
├── src/
│   └── my_game/
│       ├── __init__.py
│       ├── __main__.py
│       ├── game.py
│       ├── scenes.py
│       ├── sprites.py
│       └── assets/
└── tests/
```

Use `__main__.py` or a console script entry point:

```python
def main() -> int:
    game = Game()
    game.run()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

For uv projects, add pygame with:

```bash
uv add pygame
```

If using pygame-ce instead of pygame, be explicit and consistent:

```bash
uv add pygame-ce
```

Do not depend on both unless the project has a deliberate compatibility reason.

## Common Pygame Antipatterns

Avoid:

- Calling `pygame.init()` or `display.set_mode()` at import time.
- Loading images, sounds, or fonts every frame.
- Creating fonts every frame for static text.
- Running a busy loop without `Clock.tick()`.
- Forgetting to process events.
- Keeping all game logic in one giant file or one giant loop.
- Using globals for mutable game state when scenes/entities can own state.
- Mixing event handling, physics, drawing, asset loading, and persistence in one function.
- Using integer rect position as the only position for smooth moving entities.
- Re-scaling or rotating source images destructively every frame; keep originals and cache transformed variants when possible.
- Using pixel-perfect masks for everything.
- Blocking on file/network operations during gameplay.
- Letting entities call `pygame.display` directly; draw to the surface passed in.
- Catching all exceptions in the main loop and continuing with corrupted state.

## Refactoring Moves for Pygame Projects

- Move script-level code into `main()` and `Game.run()`.
- Extract `Scene` classes from giant mode conditionals.
- Split `handle_events()`, `update(dt)`, and `draw(surface)`.
- Introduce an asset/resource loader that caches surfaces, sounds, and fonts.
- Convert duplicated entity dictionaries into `Sprite` classes or dataclasses plus systems.
- Replace magic numbers with named constants for screen size, tile size, speeds, layers, colors, and timings.
- Move collision code into focused helpers or systems.
- Preserve public run commands and save/data formats while reorganizing internals.
- Add pure tests around logic before changing gameplay behavior.

## Review Checklist

Before reporting back:

- [ ] Main loop processes events, updates, draws, and caps FPS.
- [ ] Assets are loaded outside the per-frame path.
- [ ] Movement/timers use clear units and `dt` where appropriate.
- [ ] Scenes/states are explicit enough for the game's complexity.
- [ ] Display/audio initialization happens at the boundary.
- [ ] Core logic can be tested without a visible window when practical.
- [ ] uv or other project tooling was respected.
