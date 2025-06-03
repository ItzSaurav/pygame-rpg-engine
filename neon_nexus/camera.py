# camera.py
import pygame
import random
from error_handler import StateError

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.shake_amount = 0
        self.shake_duration = 0
        self.target_x = 0
        self.target_y = 0
        self.smoothness = 0.1
        self.offset_y = 100  # Reduced camera height offset
        self.vertical_smoothness = 0.15  # Slightly different smoothness for vertical movement
        self.debug_info = {}  # For debugging camera movement
        
        # World boundaries
        self.world_width = 4000
        self.world_height = 3000
    
    def update(self, target):
        """Update camera position"""
        try:
            # Update target position
            self.target_x = target.x - self.width // 2
            self.target_y = target.y - self.height // 2 + self.offset_y
            
            # Smoothly move towards target
            self.x += (self.target_x - self.x) * self.smoothness
            self.y += (self.target_y - self.y) * self.vertical_smoothness
            
            # Apply screen shake
            if self.shake_duration > 0:
                self.x += (pygame.random.random() * 2 - 1) * self.shake_amount
                self.y += (pygame.random.random() * 2 - 1) * self.shake_amount
                self.shake_duration -= 1
                
            # Keep camera within world boundaries
            self.x = max(0, min(self.x, self.world_width - self.width))
            self.y = max(0, min(self.y, self.world_height - self.height))
            
            # Debug info
            self.debug_info = {
                'target_x': self.target_x,
                'target_y': self.target_y,
                'camera_x': self.x,
                'camera_y': self.y,
                'player_y': target.y,
                'is_jumping': target.jumping if hasattr(target, 'jumping') else False,
                'on_ground': target.on_ground if hasattr(target, 'on_ground') else True
            }
            
            # Print debug info
            if self.debug_info:
                print("Camera Debug:", self.debug_info)
                self.debug_info = {}  # Clear debug info after printing
            
        except Exception as e:
            raise StateError(f"Failed to update camera: {str(e)}")
    
    def shake(self, amount, duration):
        """Apply screen shake effect"""
        try:
            self.shake_amount = amount
            self.shake_duration = duration
            
        except Exception as e:
            raise StateError(f"Failed to apply screen shake: {str(e)}")
    
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
        """Get the visible rectangle in world coordinates"""
        try:
            return pygame.Rect(self.x, self.y, self.width, self.height)
            
        except Exception as e:
            raise StateError(f"Failed to get visible rectangle: {str(e)}")
            
    def apply_obj(self, x, y):
        """Convert world coordinates to screen coordinates for objects"""
        return (x - self.x, y - self.y)

    def to_dict(self):
        """Convert camera state to dictionary"""
        try:
            return {
                'x': self.x,
                'y': self.y,
                'target_x': self.target_x,
                'target_y': self.target_y
            }
        except Exception as e:
            raise StateError(f"Failed to serialize camera: {str(e)}")
            
    def from_dict(self, data):
        """Load camera state from dictionary"""
        try:
            self.x = data['x']
            self.y = data['y']
            self.target_x = data['target_x']
            self.target_y = data['target_y']
            
        except Exception as e:
            raise StateError(f"Failed to deserialize camera: {str(e)}")