---
name: pygame-patterns
description: Pygame-specific best practices, architecture patterns, and antipatterns for Python games. Use when building, refactoring, debugging, or reviewing pygame projects, including game loops, sprites, scenes/states, assets, input, collision, timing, rendering, packaging, and tests.
---

# Pygame Patterns

## Purpose

Build, refactor, debug, and review pygame projects using idiomatic Python and pygame-specific practices. Use this skill with `refactor-python` when cleaning up pygame code.

Optimize for a stable main loop, explicit input/update/draw boundaries, predictable timing, cached assets, testable core logic, and architecture that fits the game's actual size.

## First Inspection Checklist

Before editing, inspect:

- Python tooling: `pyproject.toml`, `uv.lock`, `.python-version`, test config, run scripts, package layout, and supported Python versions.
- Which package is installed: `pygame` or `pygame-ce`. They both import as `pygame`; choose one and do not mix them.
- Entry point and initialization: where `pygame.init()`, mixer/display setup, `display.set_mode()`, and the main loop happen.
- Main loop order: event pumping, input handling, update timing, drawing, `display.flip()`/`update()`, and `Clock.tick()`.
- Asset paths/loading for images, sounds, fonts, maps, and data.
- Scene/state model for menus, gameplay, pause, settings, and game-over flows.
- Sprite/entity organization, collision code, coordinate system, and camera/viewport logic.
- Input model: one-shot events versus held-key state.
- Tests, headless support, and any CI constraints.

For uv projects, prefer commands like:

```bash
uv run python -m your_game
uv run pytest -q
uv run ruff check .
uv add pygame      # original package
uv add pygame-ce   # community fork
```

Do not migrate a non-uv project to uv unless asked.

## Core Shape

For small and medium games, prefer a `Game` application object plus explicit scenes/states. Keep pygame initialization and display creation at the application boundary, not import time.

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
            if self.scene.next_scene is not None:
                self.scene = self.scene.next_scene
            self.scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
```

A scene owns the sprites, UI, and transition decisions for one mode. Let the main loop perform scene swaps so scenes do not mutate each other directly.

```python
class Scene:
    def __init__(self) -> None:
        self.next_scene: "Scene | None" = None

    def handle_events(self, events) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self, surface: pygame.Surface) -> None: ...
```

Avoid one giant loop with branches for every menu, pause, gameplay, and game-over mode.

## Main Loop, Timing, and Input

- Pump events every frame with `pygame.event.get()` or equivalent; otherwise the OS may mark the window unresponsive.
- Use `pygame.time.Clock().tick(fps)` to cap frame rate and compute `dt` in seconds.
- Use `dt` for movement, cooldowns, animation timers, and other frame-rate-sensitive behavior.
- Keep loop order consistent: collect events, handle input, update simulation, draw, flip/update display.
- Draw the whole frame unless deliberately using dirty rectangles; use `display.update(rects)` only when tracking dirty regions intentionally.
- Clamp extreme `dt` values after stalls/debug pauses when large jumps would break gameplay.
- Keep shutdown explicit: exit the loop, call `pygame.quit()`, and return an exit code from `main()`.

Use events for one-shot actions such as quit, pause toggles, menu selection, clicks, and jump/button presses. Use held-key state for continuous actions:

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player.velocity.x = -PLAYER_SPEED
```

Avoid scattering direct keyboard checks across unrelated objects. Prefer a small input layer or pass actions to the objects that need them.

For high-volume events such as mouse motion or joystick axes, consider `pygame.event.set_blocked(...)` / `set_allowed(...)` only after measuring or seeing queue pressure. Never block `QUIT` or events required by the current scene/window behavior.

## Sprites and Entities

Use `pygame.sprite.Sprite` and groups when they simplify update, draw, and collision.

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=pos)
        self.position = pygame.Vector2(self.rect.center)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rect.center = round(self.position.x), round(self.position.y)
```

Guidelines:

- Keep float world positions separate from integer `Rect`s for smooth movement.
- Use `pygame.Vector2` for velocity, acceleration, direction, and camera math.
- Use groups for batch `update()`, `draw()`, and collision checks.
- Keep entities focused. Move spawning, level loading, persistence, and global orchestration to scenes/systems.
- Prefer composition once sprite inheritance becomes deep.

## Rendering and Asset Handling

Load assets once, convert them after display initialization, then reuse them.

- Do not load images, sounds, fonts, or maps inside `draw()` or per-frame `update()` paths.
- Use `.convert_alpha()` for transparent sprites and `.convert()` for opaque backgrounds.
- Cache fonts, rendered static text, and transformed images keyed by parameters.
- Keep original source images; do not destructively scale/rotate the only copy each frame.
- Centralize asset paths with `pathlib.Path` or `importlib.resources` for packaged games.
- Keep UI layout separate from gameplay simulation; use `Rect` alignment helpers for readable positioning.

Example resource helper:

```python
ASSET_DIR = Path(__file__).resolve().parent / "assets"


def load_image(name: str, *, alpha: bool = True) -> pygame.Surface:
    image = pygame.image.load(str(ASSET_DIR / name))
    return image.convert_alpha() if alpha else image.convert()
```

## Coordinates, Camera, and Collision

Keep world coordinates separate from screen coordinates. Sprites store world positions/rects; the camera converts to screen positions only at draw time.

```python
class Camera:
    def __init__(self, view_size: tuple[int, int]) -> None:
        self.offset = pygame.Vector2(0, 0)
        self.view_size = view_size

    def follow(self, target: pygame.Vector2) -> None:
        width, height = self.view_size
        self.offset.x = target.x - width / 2
        self.offset.y = target.y - height / 2

    def world_view(self) -> pygame.Rect:
        width, height = self.view_size
        return pygame.Rect(round(self.offset.x), round(self.offset.y), width, height)

    def apply(self, world_rect: pygame.Rect) -> pygame.Rect:
        return world_rect.move(-round(self.offset.x), -round(self.offset.y))
```

Guidelines:

- Cull large worlds with `camera.world_view().colliderect(sprite.rect)`, not a screen-space rect at `(0, 0)`.
- Clamp the camera to level bounds when you do not want to reveal empty space.
- Pass the camera or offset into draw methods; individual sprites should not read or mutate global camera state.
- Choose the cheapest collision that fits: `Rect`, circle/radius, spatial partition/tile broad phase, then `pygame.mask` only when pixel-perfect checks are necessary.
- Keep collision detection separate from collision response when that improves clarity.
- Keep collision resolution deterministic and simple before adding complex physics.

For arcade games, variable timestep with capped FPS is often enough. Use a fixed-step accumulator only when deterministic physics or replay/network behavior requires it.

## Audio

- Initialize the mixer deliberately if frequency, channel count, or buffer size matters.
- Load `pygame.mixer.Sound` effects once and reuse them.
- Use channels when overlapping sounds need control.
- Keep streamed music separate from short sound effects.
- Avoid blocking loads during gameplay.

## Testing and Headless Runs

Make core game behavior testable without opening a window:

- Extract pure logic for scoring, movement rules, cooldowns, state transitions, inventory, AI decisions, level parsing, and save/load.
- Keep pygame display/audio initialization at boundaries.
- Set dummy SDL drivers before pygame initialization when CI/headless tests need them:

```python
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
```

- Use `pytest` for pure logic tests.
- Avoid brittle tests that depend on exact frame timing unless timing is the behavior under test.
- Remember that `.convert()`/`.convert_alpha()` require a display surface, even if it uses the dummy video driver.

## Packaging and Layout

Prefer an importable package with an explicit entry point:

```text
project/
├── pyproject.toml
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

```python
def main() -> int:
    game = Game()
    game.run()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Preserve existing run commands, save/data formats, and public imports while reorganizing internals.

## Performance Debugging

Measure before optimizing or doing performance-driven refactors. Profiling is especially useful when touching per-frame rendering, collision, asset loading, pathfinding, or large sprite groups.

Useful tools:

- On-screen FPS overlay using `clock.get_fps()`, re-rendered only when the shown value changes.
- `cProfile` for a representative run: `uv run python -m cProfile -o game.prof -m my_game`.
- `time.perf_counter()` around suspect loop sections behind a debug flag.
- `pygame.time.get_ticks()` for coarse game-event timing.

Common hot spots:

- Unconverted surfaces.
- Per-frame `transform.scale` / `rotate` / `smoothscale` on unchanged inputs.
- Per-frame `Font.render` for text that rarely changes.
- Pixel-perfect masks where rect/radius checks suffice.
- Linear collision scans over large worlds without broad-phase filtering.
- Asset or audio loads inside `update()` / `draw()`.
- Excessive event volume that the game never consumes.

## Refactoring Moves

- Move script-level code into `main()` and `Game.run()`.
- Split `handle_events()`, `update(dt)`, and `draw(surface)`.
- Extract scenes from giant mode conditionals one mode at a time.
- Centralize asset loading and caching, then replace ad-hoc loads file by file.
- Convert duplicated entity dictionaries into sprites, dataclasses, or focused systems.
- Replace magic numbers with named constants for screen size, tile size, speeds, layers, colors, and timings.
- Separate world state from rendering; pass `surface` and camera/offset explicitly.
- Move collision code into focused helpers or systems.
- Add pure tests around game logic before changing gameplay behavior.

For large projects, do not split a god file first. Establish seams first: single initialization boundary, explicit main loop, scene interface, asset loader, and world-versus-screen coordinate boundary. Then move modules along those seams. Verify by running the game and focused tests after each step.

## Common Antipatterns

Avoid:

- Calling `pygame.init()` or `display.set_mode()` at import time.
- Forgetting to process events or running a busy loop without `Clock.tick()`.
- Loading assets, creating fonts, rendering unchanged text, or transforming unchanged images every frame.
- Keeping all game logic in one giant file or one giant loop.
- Using mutable globals for game state that scenes/entities should own.
- Mixing input, physics, drawing, asset loading, persistence, and scene transitions in one function.
- Using integer rect positions as the only positions for smooth moving entities.
- Using pixel-perfect masks for everything.
- Blocking on file/network operations during gameplay.
- Letting entities call `pygame.display` directly instead of drawing to the surface passed in.
- Catching all exceptions in the main loop and continuing with corrupted state.

## Review Checklist

Before reporting back:

- [ ] The main loop processes events, updates, draws, flips/updates display, and caps FPS.
- [ ] Assets and expensive transforms are outside per-frame paths or cached.
- [ ] Movement/timers use clear units and `dt` where appropriate.
- [ ] Scenes/states are explicit enough for the game's complexity.
- [ ] Display/audio initialization happens at the boundary.
- [ ] World and screen coordinates are not accidentally mixed.
- [ ] Core logic can be tested without a visible window when practical.
- [ ] uv or other project tooling was respected.
