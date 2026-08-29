# Pygame 2D Action RPG Engine

A top-down 2D action game engine prototype built with Python and Pygame, exploring procedural terrain generation, camera tracking, and entity state management.

## Features

- **Procedural Terrain**: Uses Perlin noise algorithms to generate continuous 2D tilemaps.
- **Camera System**: Viewport tracking centered on player position with world boundary clamping.
- **Entity Management**: Player movement, projectile physics, and enemy pathfinding/state handling.
- **Save Management**: File-based persistence for player inventory, coordinates, and game state.
- **Input Handling**: Support for keyboard/mouse and gamepad controller inputs.

## Tech Stack

- Python 3
- Pygame
- Noise (Perlin noise library)

## Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/ItzSaurav/pygame-rpg-engine.git
   cd pygame-rpg-engine
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the game:
   ```bash
   python -m neon_nexus.world
   ```

## License

MIT License.
