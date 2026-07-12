# ⚡ Neon Nexus

> A 2D action RPG with neon aesthetics, procedural worlds, and way too many particle effects.

---

## What Is This?

**Neon Nexus** is a top-down 2D action RPG built entirely in Python with Pygame. You explore procedurally generated worlds, fight enemies with melee and magic, level up, and traverse interconnected areas — forests, caves, dungeons, and villages — through gated portals that keep things interesting.

It started as a "let me see if I can build a game from scratch" project and turned into a full combat system with spells, bosses, destructible environments, and a save system that actually works. No game engine, no shortcuts — just Python and stubbornness.

## ✨ Features

- **Procedural World Generation** — Chunk-based terrain using Perlin noise. Grass, water, mountains, sand transitions — it all generates on the fly.
- **Combat System** — Melee attacks with charge-up mechanics + a spell system (fire, ice, lightning) with individual spell levels and mana management.
- **RPG Progression** — XP, leveling, stat growth (speed, health, mana scale per level), inventory system, and level-up particle effects because *why not*.
- **Multiple Area Types** — Forest, Cave, Dungeon, and Village biomes with gated transitions (key gates, boss gates, hidden walls, destructible barriers).
- **Boss Fights** — Dedicated boss enemies with their own mechanics.
- **Environmental Puzzles** — Boxes, levers, pressure plates, and destructible blocks scattered throughout the world.
- **Save/Load System** — Persistent progression via `SaveManager`. Pick up where you left off.
- **Gamepad Support** — Full joystick/controller input alongside keyboard controls.
- **Dynamic Camera** — Smooth-follow camera system that tracks the player through the world.
- **Procedural Assets** — All game sprites and menu icons are generated programmatically — no external art dependencies.
- **Error Handling** — Custom exception hierarchy (`GameError`, `ResourceError`, `SaveError`, etc.) with structured logging.

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Language | Python 3 |
| Game Framework | Pygame 2.6.1 |
| World Gen | Perlin noise (`noise` library) |
| Architecture | Modular — separate modules for player, world, camera, enemies, saves, input |
| Assets | 100% procedurally generated at runtime |

## 📁 Project Structure

```
PORT/
├── neon_nexus/
│   ├── main.py              # Game loop, menu system, state management
│   ├── player.py            # Player class — combat, spells, progression
│   ├── world.py             # Chunk-based world generation
│   ├── areas.py             # Area types, gates, biome logic
│   ├── world_map.py         # World map navigation
│   ├── enemy.py             # Enemy + Boss entities
│   ├── projectile.py        # Spell projectile physics
│   ├── portal.py            # Inter-area portals
│   ├── environment.py       # Boxes, levers, pressure plates
│   ├── camera.py            # Smooth-follow camera
│   ├── joystick.py          # Gamepad input handling
│   ├── save_manager.py      # Save/load persistence
│   ├── audio_manager.py     # Sound management
│   ├── error_handler.py     # Custom exception hierarchy + logging
│   ├── generate_assets.py   # Procedural sprite generation
│   └── generate_menu_icons.py # Menu icon generation
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

**Prerequisites:** Python 3.8+

```bash
# Clone it
git clone https://github.com/ItzSaurav/PORT.git
cd PORT

# Install dependencies
pip install -r requirements.txt

# Generate game assets
python neon_nexus/generate_assets.py
python neon_nexus/generate_menu_icons.py

# Run the game
python neon_nexus/main.py
```

That's it. No build step, no config files, no Docker — just run it.

## 🎮 Controls

| Action | Keyboard | Gamepad |
|---|---|---|
| Move | WASD / Arrow Keys | Left Stick |
| Attack | Space | A Button |
| Cast Spell | E | B Button |
| Interact | F | X Button |
| Menu | Escape | Start |

> Controller mappings are handled by `joystick.py` and should work with most standard gamepads.

## 📸 Screenshots

*Coming soon — gameplay captures and GIFs will go here.*

<!-- Add screenshots like this:
![Gameplay](screenshots/gameplay.png)
![Combat](screenshots/combat.png)
-->

---

Built by [Saurav](https://github.com/ItzSaurav) · Made with Python, Pygame, and an unreasonable amount of late nights.