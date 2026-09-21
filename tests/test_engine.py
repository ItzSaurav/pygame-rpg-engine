import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "neon_nexus"))

import pygame
import main

def test_game_loop_and_save():
    print("Initializing Game...")
    game = main.Game()
    assert game is not None
    print("Game initialized.")

    game.state = 'game'
    print("Switching state to 'game'...")

    for i in range(60):
        if i == 5:
            game.player.move('left')
        elif i == 15:
            game.player.move('right')
        elif i == 25:
            game.player.jump()

        game._update()
        game._draw()

    print(f"60 frames simulated. Player position: ({game.player.x:.1f}, {game.player.y:.1f})")

    print("Testing save_game...")
    game.save_manager.save_game(game)
    assert game.save_manager.has_save()
    print("save_game passed.")

    print("Testing load_game...")
    game.save_manager.load_game(game)
    print("load_game passed.")

    print("Testing cleanup...")
    game._cleanup()
    print("cleanup passed.")
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_game_loop_and_save()
