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
- Which pygame package: `pygame` (original) or `pygame-ce` (the actively maintained community fork). They share the `import pygame` namespace and are largely API-compatible, but versions and bug fixes diverge. Do not mix both in one project.
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

For projects with high event volume (mouse motion, joystick axes), filter what the queue carries with `pygame.event.set_blocked(...)` and `set_allowed(...)` during scene setup so the loop spends less time iterating events the game does not consume.

## Scene and State Patterns

Use explicit scenes/states for major modes:

- `TitleScene`
- `GameScene`
- `PauseScene`
- `GameOverScene`
- `SettingsScene`

A scene typically owns its sprites, UI elements, and transition decisions. Give scenes a reference to the application and an explicit transition signal so the main loop can swap them without scenes touching each other directly:

```python
class Scene:
    def __init__(self, game: "Game") -> None:
        self.game = game
        self.next_scene: Scene | None = None

    def handle_events(self, events: list[pygame.event.Event]) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
```

In `Game.run()`, after `update`, check `self.scene.next_scene` and swap if set. This keeps transitions explicit and avoids scenes constructing their successors at arbitrary points during update or draw.

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

## Camera and Viewport

For scrolling games, keep world coordinates separate from screen coordinates and apply a single offset at draw time.

```python
class Camera:
    def __init__(self, view_size: tuple[int, int]) -> None:
        self.offset = pygame.Vector2(0, 0)
        self.view = pygame.Rect((0, 0), view_size)

    def follow(self, target: pygame.Vector2) -> None:
        self.offset.x = target.x - self.view.width / 2
        self.offset.y = target.y - self.view.height / 2

    def apply(self, world_rect: pygame.Rect) -> pygame.Rect:
        return world_rect.move(-self.offset.x, -self.offset.y)
```

Guidelines:

- Sprites store world position; the camera produces screen rects only at draw time.
- Cull off-screen sprites before drawing (`self.view.colliderect(sprite.rect)`) for large levels.
- Clamp the camera to level bounds to avoid revealing empty space.
- Avoid letting individual sprites read or mutate camera state; pass the camera (or an offset) into `draw`.

## Profiling and Performance Debugging

Before optimizing or refactoring for performance, measure. Pygame projects usually have a small number of hot paths and many cheap ones.

Quick tools:

- On-screen FPS overlay using `clock.get_fps()` rendered to a cached `Surface` (re-render only when the value's integer part changes).
- `cProfile` for a representative gameplay run: `uv run python -m cProfile -o game.prof -m my_game`, then inspect with `snakeviz game.prof` or `python -m pstats game.prof`.
- `time.perf_counter()` deltas around suspect sections inside the loop, gated by a debug flag.
- `pygame.time.get_ticks()` for coarse millisecond timing of game events.

Common pygame hot spots to check first:

- Surfaces blitted without `convert()`/`convert_alpha()` (large, hidden cost).
- `pygame.transform.scale`/`rotate`/`smoothscale` called per frame on the same source — cache results keyed by parameters.
- `pygame.font.Font.render` called per frame for text whose value rarely changes.
- Pixel-perfect mask collision when a rect or radius check would suffice.
- Linear scans over large sprite groups for collision; broad-phase by zone or rect first.
- Loading audio or images inside `update`/`draw` paths.
- `pygame.event.get()` ignoring the value but pumping huge motion event volume — block what is not used.

Lock perf-relevant choices into the architecture rather than scattering optimizations: load and convert assets at boundaries, cache transforms in the asset layer, and keep the per-frame path doing only blit/update math.

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

For uv projects, add the chosen package explicitly:

```bash
uv add pygame      # original
uv add pygame-ce   # community fork (actively maintained)
```

Pick one. The two share the `pygame` import name but ship different versions; mixing them produces subtle bugs.

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

## Refactoring a Large Pygame Project

For codebases beyond a few thousand lines, work in this order. Each step lands a clean diff and unblocks the next without changing observable behavior.

1. **Pin behavior first.** Run the game, capture the boot path, and write characterization tests around any pure logic you can extract today (scoring, level parsing, save/load, AI decisions). Without these, large refactors regress silently.
2. **Profile before restructuring.** Run a representative session under `cProfile`, look at the top 10 functions by cumulative time, and note any `convert()` misses, per-frame transforms, and per-frame text renders. Refactoring blind to hot paths often makes them worse.
3. **Hoist `pygame.init()` and `display.set_mode()` to a single boundary.** Many large projects have init scattered across modules and at import time; consolidate before anything else, otherwise every later refactor fights load order.
4. **Introduce a `Game` object and an explicit scene interface** before splitting files. Move the existing main loop's branches into named scenes one at a time. Keep the old code path callable until the last branch is moved.
5. **Centralize asset loading** behind a loader that caches converted surfaces, fonts, and sounds. Replace ad-hoc `pygame.image.load` calls with the loader file by file. This usually deletes substantial duplicated code.
6. **Separate world state from rendering.** If sprites currently draw themselves using globals, give `draw(surface, camera)` an explicit signature and pass the camera/offset through. This is the change that unlocks future scene splits, headless tests, and editor tooling.
7. **Split the god file last, not first.** Once boundaries above are clean, move modules along the seams already present (scenes/, entities/, systems/, ui/, assets/). Splitting before the seams exist creates a tangle of cross-module imports.
8. **Verify each step.** Run the game and the focused tests after every move. With pygame, a regression is often a missing `convert_alpha()`, a swallowed event, or a frame-rate-dependent jump that only shows on someone else's machine — catch these one change at a time.

Avoid: rewriting the loop and the asset pipeline and the scene system in one branch. The diff becomes unreviewable and bisecting regressions becomes painful.

## Review Checklist

Before reporting back:

- [ ] Main loop processes events, updates, draws, and caps FPS.
- [ ] Assets are loaded outside the per-frame path.
- [ ] Movement/timers use clear units and `dt` where appropriate.
- [ ] Scenes/states are explicit enough for the game's complexity.
- [ ] Display/audio initialization happens at the boundary.
- [ ] Core logic can be tested without a visible window when practical.
- [ ] uv or other project tooling was respected.
