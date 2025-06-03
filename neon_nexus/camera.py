# camera.py
import pygame

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.smooth_follow = True
        self.follow_speed = 0.1  # Lower = smoother
        
    def update(self, target):
        if self.smooth_follow:
            # Calculate target position
            target_x = target.x - self.screen_width // 2
            target_y = target.y - self.screen_height // 2
            
            # Smoothly interpolate to target position
            self.x += (target_x - self.x) * self.follow_speed
            self.y += (target_y - self.y) * self.follow_speed
        else:
            # Direct follow
            self.x = target.x - self.screen_width // 2
            self.y = target.y - self.screen_height // 2
        
        # Keep camera within world boundaries
        self.x = max(0, min(self.x, self.world_width - self.screen_width))
        self.y = max(0, min(self.y, self.world_height - self.screen_height))
        
    def apply(self, entity):
        # Convert world coordinates to screen coordinates with zoom
        screen_x = (entity.x - self.x) * self.zoom
        screen_y = (entity.y - self.y) * self.zoom
        return (screen_x, screen_y)
    
    def apply_rect(self, rect):
        # Convert a rectangle from world coordinates to screen coordinates
        x, y = self.apply(rect)
        return pygame.Rect(x, y, rect.width * self.zoom, rect.height * self.zoom)
    
    def get_visible_rect(self):
        # Return the visible area in world coordinates
        return pygame.Rect(
            self.x,
            self.y,
            self.screen_width / self.zoom,
            self.screen_height / self.zoom
        )
    
    def zoom_in(self, factor=1.1):
        self.zoom = min(self.zoom * factor, 2.0)
    
    def zoom_out(self, factor=0.9):
        self.zoom = max(self.zoom * factor, 0.5)