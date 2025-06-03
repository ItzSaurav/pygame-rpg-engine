import pygame
import math

class WorldMap:
    def __init__(self, world_width, world_height, chunk_size):
        self.world_width = world_width
        self.world_height = world_height
        self.chunk_size = chunk_size
        
        # Calculate grid dimensions
        self.grid_width = world_width // chunk_size
        self.grid_height = world_height // chunk_size
        
        # Map state
        self.visited_chunks = set()  # Set of (x, y) chunk coordinates
        self.current_chunk = (0, 0)
        
        # UI settings
        self.visible = False
        self.map_scale = 0.2  # Scale of the minimap relative to screen
        self.blink_timer = 0
        self.blink_speed = 30  # Frames per blink
        self.map_padding = 20  # Padding from screen edges
        
        # Colors
        self.colors = {
            'background': (20, 20, 40, 200),
            'grid': (100, 100, 100, 100),
            'visited': (100, 200, 255, 150),
            'current': (255, 255, 100, 255),
            'border': (255, 255, 255, 100)
        }
        
        # Create map surface
        self.map_width = int(self.world_width * self.map_scale)
        self.map_height = int(self.world_height * self.map_scale)
        self.map_surface = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)
    
    def toggle(self):
        """Toggle map visibility"""
        self.visible = not self.visible
    
    def update_current_chunk(self, x, y):
        """Update the current chunk position"""
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        self.current_chunk = (chunk_x, chunk_y)
        self.visited_chunks.add(self.current_chunk)
    
    def mark_chunk_visited(self, chunk_x, chunk_y):
        """Mark a chunk as visited"""
        self.visited_chunks.add((chunk_x, chunk_y))
    
    def _draw_grid(self):
        """Draw the grid lines on the map"""
        # Clear the map surface
        self.map_surface.fill((0, 0, 0, 0))
        
        # Draw background
        pygame.draw.rect(self.map_surface, self.colors['background'], 
                        self.map_surface.get_rect())
        
        # Draw grid lines
        for x in range(0, self.map_width + 1, int(self.chunk_size * self.map_scale)):
            pygame.draw.line(self.map_surface, self.colors['grid'], 
                           (x, 0), (x, self.map_height))
        for y in range(0, self.map_height + 1, int(self.chunk_size * self.map_scale)):
            pygame.draw.line(self.map_surface, self.colors['grid'], 
                           (0, y), (self.map_width, y))
        
        # Draw visited chunks
        for chunk_x, chunk_y in self.visited_chunks:
            rect = pygame.Rect(
                chunk_x * self.chunk_size * self.map_scale,
                chunk_y * self.chunk_size * self.map_scale,
                self.chunk_size * self.map_scale,
                self.chunk_size * self.map_scale
            )
            pygame.draw.rect(self.map_surface, self.colors['visited'], rect)
        
        # Draw current chunk
        if self.blink_timer < self.blink_speed // 2:  # Blink effect
            current_rect = pygame.Rect(
                self.current_chunk[0] * self.chunk_size * self.map_scale,
                self.current_chunk[1] * self.chunk_size * self.map_scale,
                self.chunk_size * self.map_scale,
                self.chunk_size * self.map_scale
            )
            pygame.draw.rect(self.map_surface, self.colors['current'], current_rect)
        
        # Draw border
        pygame.draw.rect(self.map_surface, self.colors['border'], 
                        self.map_surface.get_rect(), 2)
    
    def update(self):
        """Update map state"""
        if not self.visible:
            return
        
        # Update blink timer
        self.blink_timer = (self.blink_timer + 1) % self.blink_speed
        
        # Redraw the map
        self._draw_grid()
    
    def draw(self, screen):
        """Draw the map on the screen"""
        if not self.visible:
            return
        
        # Calculate position (top-right corner)
        map_x = screen.get_width() - self.map_width - self.map_padding
        map_y = self.map_padding
        
        # Draw map
        screen.blit(self.map_surface, (map_x, map_y))
    
    def to_dict(self):
        """Convert map data to dictionary for saving"""
        return {
            'visited_chunks': list(self.visited_chunks),
            'current_chunk': self.current_chunk
        }
    
    @classmethod
    def from_dict(cls, data, world_width, world_height, chunk_size):
        """Create map from saved data"""
        world_map = cls(world_width, world_height, chunk_size)
        world_map.visited_chunks = set(tuple(chunk) for chunk in data['visited_chunks'])
        world_map.current_chunk = tuple(data['current_chunk'])
        return world_map 