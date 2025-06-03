import pygame
import math

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed, damage, spell_type="fire"):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.speed = speed
        self.damage = damage
        self.spell_type = spell_type
        self.lifetime = 60  # Frames before projectile disappears
        self.active = True
        
        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        length = math.sqrt(dx * dx + dy * dy)
        self.dx = (dx / length) * speed if length > 0 else 0
        self.dy = (dy / length) * speed if length > 0 else 0
        
        # Create projectile surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_projectile()
    
    def _draw_projectile(self):
        # Draw different projectiles based on spell type
        if self.spell_type == "fire":
            # Fire projectile (orange with glow)
            pygame.draw.circle(self.surface, (255, 100, 0), (self.width//2, self.height//2), 6)
            pygame.draw.circle(self.surface, (255, 200, 0), (self.width//2, self.height//2), 4)
            # Add glow effect
            glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 100, 0, 50), (self.width//2, self.height//2), 8)
            self.surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        elif self.spell_type == "ice":
            # Ice projectile (blue with glow)
            pygame.draw.circle(self.surface, (100, 200, 255), (self.width//2, self.height//2), 6)
            pygame.draw.circle(self.surface, (200, 255, 255), (self.width//2, self.height//2), 4)
            # Add glow effect
            glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(glow, (100, 200, 255, 50), (self.width//2, self.height//2), 8)
            self.surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        elif self.spell_type == "lightning":
            # Lightning projectile (yellow with glow)
            pygame.draw.circle(self.surface, (255, 255, 100), (self.width//2, self.height//2), 6)
            pygame.draw.circle(self.surface, (255, 255, 200), (self.width//2, self.height//2), 4)
            # Add glow effect
            glow = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 255, 100, 50), (self.width//2, self.height//2), 8)
            self.surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
    def update(self):
        if not self.active:
            return
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Update lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False
    
    def draw(self, screen, camera):
        if not self.active:
            return
        
        # Calculate screen position
        screen_x, screen_y = camera.apply(self)
        
        # Draw projectile
        screen.blit(self.surface, (screen_x, screen_y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height) 