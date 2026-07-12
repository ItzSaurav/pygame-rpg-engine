# Neon Nexus (PORT)

A top-down action game developed in Python, featuring dynamic combat, exploration, and generated assets.

## 🌟 The Problem Solved

Game development from scratch involves orchestrating various systems like rendering, input, and physics. "Neon Nexus" is a custom-built game engine and interactive experience demonstrating game loop mechanics, asset generation, camera systems, and entity management (players & enemies) using Python.

## 🛠️ Tech Stack

- **Language**: Python 3
- **Libraries**: Relies on standard libraries and Python game frameworks (dependencies listed in `requirements.txt`)
- **Architecture**: Modular design separating `player`, `enemy`, `camera`, `joystick`, and `world` logic.

## ✨ Features

- **Dynamic Camera System**: Follows the player and manages the viewport (`camera.py`).
- **Entity Management**: Separate modules for player actions, enemies, and projectiles.
- **World & Environment**: Tile-based or continuous world mapping (`world.py`, `world_map.py`, `areas.py`).
- **Asset Generation**: Includes scripts to procedurally generate in-game assets and menus (`generate_assets.py`, `generate_menu_icons.py`).
- **Audio & Save States**: Built-in audio manager and save manager for persistent progression.

## 🚦 Setup Instructions

To run Neon Nexus locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/ItzSaurav/PORT.git
   ```
2. Navigate to the project directory:
   ```bash
   cd PORT
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate the necessary game assets before running:
   ```bash
   python neon_nexus/generate_assets.py
   python neon_nexus/generate_menu_icons.py
   ```
5. Launch the game:
   ```bash
   python neon_nexus/main.py
   ```

## 📸 Screenshots

*(Add screenshots or GIFs of gameplay here)*

---
*Built with ❤️ by [Saurav](https://github.com/ItzSaurav)*