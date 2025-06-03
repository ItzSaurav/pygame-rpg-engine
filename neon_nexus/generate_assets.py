import random
from PIL import Image, ImageDraw
import os
import sys
import pygame
import math

def ensure_assets_directory():
    """Ensure the assets directory exists"""
    if not os.path.exists('neon_nexus/assets'):
        os.makedirs('neon_nexus/assets')

def create_player_image():
    """Create a warrior sprite with katana and animation frames"""
    try:
        # Create a 64x64 surface for each frame (4 frames: idle, walk1, walk2, landing)
        frames = []
        for frame in range(4):
            surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            
            # Body color (dark blue armor)
            body_color = (30, 40, 80) if frame == 0 else (40, 50, 90)
            
            # Draw body (armor)
            pygame.draw.rect(surface, body_color, (24, 20, 16, 30))
            
            # Draw head (helmet)
            helmet_color = (60, 60, 60)
            pygame.draw.rect(surface, helmet_color, (26, 10, 12, 12))
            
            # Draw face (visible through helmet)
            face_color = (200, 180, 150)
            pygame.draw.rect(surface, face_color, (28, 12, 8, 8))
            
            # Draw eyes
            eye_color = (255, 255, 255)
            eye_offset = 1 if frame == 0 else 0
            pygame.draw.rect(surface, eye_color, (30, 14, 2, 2))
            pygame.draw.rect(surface, eye_color, (36, 14, 2, 2))
            
            # Draw katana
            katana_color = (200, 200, 200)
            handle_color = (139, 69, 19)
            
            # Katana blade
            if frame == 0:  # Idle
                pygame.draw.rect(surface, katana_color, (40, 20, 4, 20))
                pygame.draw.rect(surface, handle_color, (40, 18, 4, 4))
            elif frame == 3:  # Landing
                pygame.draw.rect(surface, katana_color, (42, 15, 4, 25))
                pygame.draw.rect(surface, handle_color, (42, 13, 4, 4))
            else:  # Walking
                pygame.draw.rect(surface, katana_color, (40, 20, 4, 20))
                pygame.draw.rect(surface, handle_color, (40, 18, 4, 4))
            
            # Draw arms
            arm_color = (40, 50, 90)
            if frame == 0:  # Idle
                pygame.draw.rect(surface, arm_color, (20, 22, 4, 12))
                pygame.draw.rect(surface, arm_color, (40, 22, 4, 12))
            elif frame == 3:  # Landing
                pygame.draw.rect(surface, arm_color, (20, 22, 4, 12))
                pygame.draw.rect(surface, arm_color, (38, 15, 4, 12))
            else:  # Walking
                arm_offset = 2 if frame == 1 else -2
                pygame.draw.rect(surface, arm_color, (20, 22 + arm_offset, 4, 12))
                pygame.draw.rect(surface, arm_color, (40, 22 - arm_offset, 4, 12))
            
            # Draw legs
            leg_color = (30, 40, 80)
            if frame == 0:  # Idle
                pygame.draw.rect(surface, leg_color, (26, 50, 6, 12))
                pygame.draw.rect(surface, leg_color, (32, 50, 6, 12))
            elif frame == 3:  # Landing
                pygame.draw.rect(surface, leg_color, (24, 50, 6, 12))
                pygame.draw.rect(surface, leg_color, (34, 50, 6, 12))
            else:  # Walking
                leg_offset = 4 if frame == 1 else -4
                pygame.draw.rect(surface, leg_color, (26, 50 + leg_offset, 6, 12))
                pygame.draw.rect(surface, leg_color, (32, 50 - leg_offset, 6, 12))
            
            # Add glow effect
            glow_surface = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (100, 150, 255, 30), (32, 32), 25)
            surface.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            frames.append(surface)
        
        # Save each frame
        for i, frame in enumerate(frames):
            pygame.image.save(frame, f'neon_nexus/assets/player_{i}.png')
        print("Warrior sprites generated successfully")
        
    except Exception as e:
        print(f"Error generating warrior sprite: {e}")

def create_grass_image():
    """Create a grass tile with more detail"""
    try:
        surface = pygame.Surface((32, 32))
        # Base color
        surface.fill((34, 139, 34))
        
        # Add grass blades
        for _ in range(20):
            x = random.randint(0, 31)
            y = random.randint(0, 31)
            height = random.randint(3, 8)
            color = (50, 205, 50)
            pygame.draw.line(surface, color, (x, y), (x, y - height), 1)
        
        pygame.image.save(surface, 'neon_nexus/assets/grass.png')
        print("Grass tile generated successfully")
        
    except Exception as e:
        print(f"Error generating grass tile: {e}")

def create_water_image():
    """Create a water tile with wave effect"""
    try:
        surface = pygame.Surface((32, 32))
        # Base color
        surface.fill((0, 105, 148))
        
        # Add wave patterns
        for y in range(0, 32, 4):
            for x in range(0, 32, 4):
                if (x + y) % 8 == 0:
                    pygame.draw.circle(surface, (0, 191, 255), (x, y), 2)
        
        pygame.image.save(surface, 'neon_nexus/assets/water.png')
        print("Water tile generated successfully")
        
    except Exception as e:
        print(f"Error generating water tile: {e}")

def create_sand_image():
    """Create a sand tile with texture"""
    try:
        surface = pygame.Surface((32, 32))
        # Base color
        surface.fill((194, 178, 128))
        
        # Add sand texture
        for _ in range(50):
            x = random.randint(0, 31)
            y = random.randint(0, 31)
            color = (210, 180, 140)
            pygame.draw.circle(surface, color, (x, y), 1)
        
        pygame.image.save(surface, 'neon_nexus/assets/sand.png')
        print("Sand tile generated successfully")
        
    except Exception as e:
        print(f"Error generating sand tile: {e}")

def create_mountain_image():
    try:
        # Create a 32x32 image with a gray mountain
        img = Image.new('RGB', (32, 32), (139, 137, 137))
        draw = ImageDraw.Draw(img)
        # Draw a simple mountain shape
        draw.polygon([(4,28), (16,6), (28,28)], fill=(169,169,169))
        draw.polygon([(10,20), (16,10), (22,20)], fill=(211,211,211))
        img.save('neon_nexus/assets/mountain.png')
        print("Generated mountain.png successfully")
    except Exception as e:
        print(f"Error generating mountain.png: {e}")

def create_player_sprite_sheet():
    try:
        # 2 frames, each 32x32, side by side (64x32)
        img = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Frame 0: standing
        # Head
        draw.rectangle([12, 2, 19, 9], fill=(255, 220, 180, 255))
        # Body
        draw.rectangle([14, 10, 17, 22], fill=(0, 120, 255, 255))
        # Arms
        draw.rectangle([11, 12, 13, 18], fill=(255, 220, 180, 255))
        draw.rectangle([18, 12, 20, 18], fill=(255, 220, 180, 255))
        # Legs together
        draw.rectangle([14, 23, 15, 30], fill=(60, 60, 60, 255))
        draw.rectangle([16, 23, 17, 30], fill=(60, 60, 60, 255))
        # Frame 1: walking (legs apart)
        offset = 32
        # Head
        draw.rectangle([12+offset, 2, 19+offset, 9], fill=(255, 220, 180, 255))
        # Body
        draw.rectangle([14+offset, 10, 17+offset, 22], fill=(0, 120, 255, 255))
        # Arms
        draw.rectangle([11+offset, 12, 13+offset, 18], fill=(255, 220, 180, 255))
        draw.rectangle([18+offset, 12, 20+offset, 18], fill=(255, 220, 180, 255))
        # Legs apart
        draw.rectangle([13+offset, 23, 14+offset, 30], fill=(60, 60, 60, 255))
        draw.rectangle([17+offset, 23, 18+offset, 30], fill=(60, 60, 60, 255))
        img.save('neon_nexus/assets/player.png')
        print("Generated pixel-art player sprite sheet as player.png successfully")
    except Exception as e:
        print(f"Error generating player sprite sheet: {e}")

def main():
    ensure_assets_directory()
    create_player_image()
    create_grass_image()
    create_water_image()
    create_sand_image()
    create_mountain_image()
    print("\nAll assets generated successfully!")

if __name__ == "__main__":
    main() 