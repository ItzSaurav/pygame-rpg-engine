# Neon Nexus - 2D Pygame RPG Engine

A 2D top-down action RPG prototype built from scratch in Python and Pygame, exploring procedural world generation, camera tracking, projectile physics, and file-based save states.

---

## Why I Built This

Most software engineering coursework focuses on web APIs and relational database tables. I built Neon Nexus to understand how games work under the hood: maintaining a steady 60 frames per second loop, calculating delta-time physics, mapping camera viewports onto larger worlds, and generating organic procedural terrain using Perlin noise instead of hardcoding static levels.

---

## Core Systems & Architecture

- **Game Loop & Timing (`main.py`)**: Fixed 60 FPS update loop with Pygame event dispatching, state management (Title Menu, Game World, Pause, Settings), and global exception handling.
- **Procedural World Generation (`world.py`)**: Generates large tile-based maps dynamically using 2D Perlin noise to establish biome elevation, terrain boundaries, and obstacle placement.
- **Dynamic Camera Viewport (`camera.py`)**: Smoothly interpolates and centers the camera on the player while clamping within world borders to avoid rendering out-of-bounds space.
- **Player & Combat (`player.py`, `projectile.py`, `enemy.py`)**: Multi-directional movement, collision detection with environment hitboxes, aiming vectors, and projectile spawning.
- **Save State Manager (`save_manager.py`)**: Serializes player coordinates, inventory, health, and current level progression into local JSON save slots with checksum verification.
- **Gamepad & Input (`joystick.py`)**: Flexible input abstraction layer supporting both keyboard/mouse and native analog game controllers.

---

## Tech Stack

- **Language**: Python 3.9+
- **Core Engine**: Pygame (Surface rendering, clock management, mixer audio)
- **Procedural Generation**: `noise` (Perlin noise algorithm)
- **Persistence**: JSON file I/O

---

## Project Structure

```text
pygame-rpg-engine/
├── neon_nexus/
│   ├── main.py               # Main entry point and state machine loop
│   ├── player.py             # Player movement, stats, and rendering
│   ├── world.py              # Procedural terrain generation using noise
│   ├── camera.py             # Viewport tracking and screen projection
│   ├── enemy.py              # Enemy state machines and path behavior
│   ├── projectile.py         # Bullet physics and collision checks
│   ├── save_manager.py       # JSON save slot serialization
│   ├── joystick.py           # Controller and gamepad mapping
│   ├── audio_manager.py      # Sound effects and background music
│   └── assets/               # Sprites, tiles, and sound resources
├── requirements.txt          # Python dependencies (pygame, noise)
└── README.md                 # Project documentation
```

---

## Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/ItzSaurav/pygame-rpg-engine.git
cd pygame-rpg-engine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Game
```bash
python neon_nexus/main.py
```

### Controls
- **W, A, S, D** or **Arrow Keys**: Move character
- **Mouse / Left Click**: Aim and fire projectiles
- **Escape**: Pause menu
- **Controller**: Left stick to move, right trigger / button to attack

---

## License

MIT License. Free for educational and game development learning.
