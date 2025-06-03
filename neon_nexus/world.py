# world.py
import random
import pygame
from collections import defaultdict

class Chunk:
    def __init__(self, x, y, size=32):
        self.x = x
        self.y = y
        self.size = size
        self.tiles = [[None for _ in range(size)] for _ in range(size)]
        self.generated = False
        self.entities = []
    
    def generate(self, seed=None):
        if self.generated:
            return
            
        if seed is not None:
            random.seed(seed + self.x * 1000 + self.y)
            
        # Generate terrain for this chunk
        for y in range(self.size):
            for x in range(self.size):
                # Base terrain is grass
                self.tiles[y][x] = 'grass'
                
                # Add some random features
                if random.random() < 0.02:  # 2% chance for water
                    self.tiles[y][x] = 'water'
                elif random.random() < 0.01:  # 1% chance for mountain
                    self.tiles[y][x] = 'mountain'
                    
        # Ensure chunk edges connect smoothly
        self._smooth_edges()
        self.generated = True
    
    def _smooth_edges(self):
        # Smooth transitions between chunks
        for y in range(self.size):
            for x in range(self.size):
                if x == 0 or y == 0 or x == self.size-1 or y == self.size-1:
                    if self.tiles[y][x] == 'water':
                        # Add sand around water at edges
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                nx, ny = x + dx, y + dy
                                if (0 <= nx < self.size and 0 <= ny < self.size and 
                                    self.tiles[ny][nx] == 'grass'):
                                    self.tiles[ny][nx] = 'sand'

class World:
    def __init__(self, chunk_size=32):
        self.chunk_size = chunk_size
        self.chunks = defaultdict(lambda: None)
        self.tile_size = 32
        self.seed = random.randint(0, 1000000)
        
        # Load tile images
        self.tile_images = {
            'grass': pygame.image.load('neon_nexus/assets/grass.png').convert(),
            'water': pygame.image.load('neon_nexus/assets/water.png').convert(),
            'mountain': pygame.Surface((32, 32)).convert()  # Placeholder for mountain
        }
        # Set mountain color
        self.tile_images['mountain'].fill((139, 137, 137))
    
    def get_chunk(self, x, y):
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        chunk_key = (chunk_x, chunk_y)
        
        if self.chunks[chunk_key] is None:
            self.chunks[chunk_key] = Chunk(chunk_x, chunk_y, self.chunk_size)
            self.chunks[chunk_key].generate(self.seed)
            
        return self.chunks[chunk_key]
    
    def get_tile(self, x, y):
        chunk = self.get_chunk(x, y)
        local_x = x % self.chunk_size
        local_y = y % self.chunk_size
        return chunk.tiles[local_y][local_x]
    
    def draw(self, screen, camera):
        # Get visible area in world coordinates
        visible = camera.get_visible_rect()
        
        # Calculate chunk range to render
        start_chunk_x = int(visible.left // self.chunk_size)
        end_chunk_x = int(visible.right // self.chunk_size) + 1
        start_chunk_y = int(visible.top // self.chunk_size)
        end_chunk_y = int(visible.bottom // self.chunk_size) + 1
        
        # Draw visible chunks
        for chunk_y in range(start_chunk_y, end_chunk_y):
            for chunk_x in range(start_chunk_x, end_chunk_x):
                chunk = self.get_chunk(chunk_x * self.chunk_size, 
                                     chunk_y * self.chunk_size)
                
                # Draw each tile in the chunk
                for y in range(self.chunk_size):
                    for x in range(self.chunk_size):
                        world_x = chunk_x * self.chunk_size + x
                        world_y = chunk_y * self.chunk_size + y
                        
                        # Convert to screen coordinates
                        screen_x = (world_x * self.tile_size - camera.x) * camera.zoom
                        screen_y = (world_y * self.tile_size - camera.y) * camera.zoom
                        
                        # Only draw if on screen
                        if (0 <= screen_x < camera.screen_width and 
                            0 <= screen_y < camera.screen_height):
                            terrain = chunk.tiles[y][x]
                            # Scale the image according to zoom
                            scaled_size = int(self.tile_size * camera.zoom)
                            scaled_image = pygame.transform.scale(
                                self.tile_images[terrain], 
                                (scaled_size, scaled_size)
                            )
                            screen.blit(scaled_image, (screen_x, screen_y))
    
    def unload_distant_chunks(self, center_x, center_y, keep_distance=3):
        # Unload chunks that are too far from the player
        chunks_to_keep = set()
        for chunk_y in range(-keep_distance, keep_distance + 1):
            for chunk_x in range(-keep_distance, keep_distance + 1):
                center_chunk_x = center_x // self.chunk_size
                center_chunk_y = center_y // self.chunk_size
                chunks_to_keep.add((center_chunk_x + chunk_x, 
                                  center_chunk_y + chunk_y))
        
        # Remove chunks that are too far
        for chunk_key in list(self.chunks.keys()):
            if chunk_key not in chunks_to_keep:
                del self.chunks[chunk_key]