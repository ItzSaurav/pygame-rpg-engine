# camera.py
import pygame
import random

class Camera:
    def __init__(self, target):
        self.target = target
        self.x = 0
        self.y = 0
        self.smoothness = 0.1  # Lower = smoother
        self.shake_amount = 0
        self.shake_duration = 0
        self.offset_y = 100  # Reduced camera height offset
        self.vertical_smoothness = 0.15  # Slightly different smoothness for vertical movement
        self.debug_info = {}  # For debugging camera movement
        
        # Screen dimensions
        self.width = 800
        self.height = 600
        
        # World boundaries
        self.world_width = 4000
        self.world_height = 3000
    
    def update(self):
        # Calculate target position (centered on player)
        target_x = self.target.x - self.width // 2
        target_y = self.target.y - self.height // 2 + self.offset_y
        
        # Smoothly interpolate to target position with different smoothness for vertical movement
        self.x += (target_x - self.x) * self.smoothness
        self.y += (target_y - self.y) * self.vertical_smoothness
        
        # Apply camera shake if active
        if self.shake_duration > 0:
            self.shake_amount = max(0, self.shake_amount - 0.5)
            self.shake_duration -= 1
            self.x += random.uniform(-self.shake_amount, self.shake_amount)
            self.y += random.uniform(-self.shake_amount, self.shake_amount)
        
        # Keep camera within world boundaries
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))
        
        # Debug info
        self.debug_info = {
            'target_x': target_x,
            'target_y': target_y,
            'camera_x': self.x,
            'camera_y': self.y,
            'player_y': self.target.y,
            'is_jumping': self.target.jumping if hasattr(self.target, 'jumping') else False,
            'on_ground': self.target.on_ground if hasattr(self.target, 'on_ground') else True
        }
        
        # Print debug info
        if self.debug_info:
            print("Camera Debug:", self.debug_info)
            self.debug_info = {}  # Clear debug info after printing
    
    def shake(self, amount, duration):
        """Add camera shake effect"""
        self.shake_amount = amount
        self.shake_duration = duration
    
    def apply(self, entity):
        """Convert world coordinates to screen coordinates"""
        if hasattr(entity, 'rect'):
            return (entity.rect.x - self.x, entity.rect.y - self.y)
        return (entity.x - self.x, entity.y - self.y)
    
    def apply_rect(self, rect):
        """Convert world rectangle to screen rectangle"""
        return pygame.Rect(
            int(rect.x - self.x),
            int(rect.y - self.y),
            rect.width,
            rect.height
        )
    
    def get_visible_rect(self):
        # Return the visible area in world coordinates
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def apply_obj(self, x, y):
        """Convert world coordinates to screen coordinates for objects"""
        return (x - self.x, y - self.y)