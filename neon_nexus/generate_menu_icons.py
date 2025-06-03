import pygame
import os
import math

def ensure_assets_dir():
    """Create assets directory if it doesn't exist"""
    if not os.path.exists('neon_nexus/assets'):
        os.makedirs('neon_nexus/assets')

def create_menu_icons():
    """Create icons for the main menu"""
    ensure_assets_dir()
    
    # Icon size
    size = 32
    
    # Colors
    NEON_BLUE = (100, 200, 255)
    NEON_PINK = (255, 100, 200)
    NEON_GREEN = (100, 255, 100)
    NEON_YELLOW = (255, 255, 100)
    NEON_RED = (255, 100, 100)
    
    # Create new game icon (plus symbol)
    new_game = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.line(new_game, NEON_BLUE, (size//2, size//4), (size//2, 3*size//4), 4)
    pygame.draw.line(new_game, NEON_BLUE, (size//4, size//2), (3*size//4, size//2), 4)
    pygame.image.save(new_game, 'neon_nexus/assets/new_game.png')
    
    # Create continue icon (play symbol)
    continue_icon = pygame.Surface((size, size), pygame.SRCALPHA)
    points = [(size//4, size//4), (3*size//4, size//2), (size//4, 3*size//4)]
    pygame.draw.polygon(continue_icon, NEON_GREEN, points)
    pygame.image.save(continue_icon, 'neon_nexus/assets/continue.png')
    
    # Create settings icon (gear)
    settings = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (size//2, size//2)
    radius = size//3
    pygame.draw.circle(settings, NEON_YELLOW, center, radius, 2)
    for i in range(8):
        angle = i * (360/8)
        rad = angle * (3.14159/180)
        x = center[0] + (radius + 4) * math.cos(rad)
        y = center[1] + (radius + 4) * math.sin(rad)
        pygame.draw.circle(settings, NEON_YELLOW, (int(x), int(y)), 2)
    pygame.image.save(settings, 'neon_nexus/assets/settings.png')
    
    # Create controls icon (keyboard)
    controls = pygame.Surface((size, size), pygame.SRCALPHA)
    key_size = size//4
    for i in range(3):
        for j in range(2):
            x = size//4 + i * key_size
            y = size//4 + j * key_size
            pygame.draw.rect(controls, NEON_PINK, (x, y, key_size-2, key_size-2), 1)
    pygame.image.save(controls, 'neon_nexus/assets/controls.png')
    
    # Create quit icon (X)
    quit_icon = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.line(quit_icon, NEON_RED, (size//4, size//4), (3*size//4, 3*size//4), 4)
    pygame.draw.line(quit_icon, NEON_RED, (3*size//4, size//4), (size//4, 3*size//4), 4)
    pygame.image.save(quit_icon, 'neon_nexus/assets/quit.png')

if __name__ == "__main__":
    pygame.init()
    create_menu_icons()
    pygame.quit() 