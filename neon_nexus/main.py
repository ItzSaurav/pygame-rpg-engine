import pygame
import sys
from player import Player
from camera import Camera
from world import World

# Constants
WORLD_WIDTH = 4000
WORLD_HEIGHT = 3000
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Neon Nexus")
clock = pygame.time.Clock()

# Initialize game objects
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
world = World()
all_entities = [player]  # Add more entities as needed

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle zoom with mouse wheel
            if event.button == 4:  # Scroll up
                camera.zoom_in()
            elif event.button == 5:  # Scroll down
                camera.zoom_out()
    
    # Handle player input
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    player.move(dx, dy)
    
    # Update
    camera.update(player)
    
    # Unload distant chunks to save memory
    world.unload_distant_chunks(player.x, player.y)
    
    # Draw
    screen.fill((0, 0, 0))  # Clear screen
    
    # Draw world
    world.draw(screen, camera)
    
    # Draw entities
    for entity in all_entities:
        entity.draw(screen, camera)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level: {player.level}", True, (255, 255, 255))
    xp_text = font.render(f"XP: {player.xp}", True, (255, 255, 255))
    zoom_text = font.render(f"Zoom: {camera.zoom:.1f}x", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))
    screen.blit(xp_text, (10, 50))
    screen.blit(zoom_text, (10, 90))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()