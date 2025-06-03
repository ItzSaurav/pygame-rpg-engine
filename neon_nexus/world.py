# world.py
import random
import pygame
from collections import defaultdict
import noise
import math
from areas import Area, AreaType, GateType
from world_map import WorldMap
from portal import Portal
from environment import Box, Lever, PressurePlate, DestructibleBlock
from enemy import Enemy, Boss
from error_handler import WorldError

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
    def __init__(self, width, height, chunk_size):
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.areas = {}
        self.gates = {}
        self.visited_chunks = set()
        self.world_map = WorldMap(width, height, chunk_size)
        self.portals = []  # List of portals
        self.boxes = []
        self.levers = []
        self.plates = []
        self.destructibles = []
        self.enemies = []
        self.bosses = []
        # Place a default portal in the spawn chunk (0,0)
        self.portals.append(Portal(0, 0, self.chunk_size // 2, self.chunk_size // 2, name="Spawn Portal"))
        # Example: Add a portal, box, lever, destructible, enemy, boss
        self.portals.append(Portal(2, 2, 10, 10, name="Forest Portal"))
        self.boxes.append(Box(100, 120))
        self.levers.append(Lever(140, 120))
        self.plates.append(PressurePlate(180, 120))
        self.destructibles.append(DestructibleBlock(220, 120, hp=3))
        self.enemies.append(Enemy(300, 120, enemy_type="slime"))
        self.bosses.append(Boss(400, 120, boss_type="golem"))
        # Initialize areas
        for area_type in AreaType:
            self.areas[area_type] = Area(area_type)
            self.areas[area_type].generate_gates(
                self.chunk_size,
                self.width,
                self.height
            )
        # Load tile images
        self.tile_images = {
            'grass': pygame.Surface((self.chunk_size, self.chunk_size)),
            'water': pygame.Surface((self.chunk_size, self.chunk_size)),
            'sand': pygame.Surface((self.chunk_size, self.chunk_size)),
            'stone': pygame.Surface((self.chunk_size, self.chunk_size)),
            'brick': pygame.Surface((self.chunk_size, self.chunk_size)),
            'path': pygame.Surface((self.chunk_size, self.chunk_size))
        }
        # Set tile colors
        self.tile_images['grass'].fill((100, 200, 100))
        self.tile_images['water'].fill((100, 100, 255))
        self.tile_images['sand'].fill((200, 200, 100))
        self.tile_images['stone'].fill((150, 150, 150))
        self.tile_images['brick'].fill((200, 100, 100))
        self.tile_images['path'].fill((200, 200, 200))
    
    def get_chunk(self, x, y):
        """Get or create a chunk at the specified coordinates"""
        try:
            chunk_key = (x, y)
            if chunk_key not in self.areas:
                self.areas[chunk_key] = Area(x, y, self.chunk_size)
            return self.areas[chunk_key]
        except Exception as e:
            raise WorldError(f"Failed to get chunk at ({x}, {y}): {str(e)}")
    
    def update(self, camera, player):
        """Update world state"""
        try:
            # Update current chunk
            chunk_x = int(player.x // self.chunk_size)
            chunk_y = int(player.y // self.chunk_size)
            self.visited_chunks.add((chunk_x, chunk_y))
            
            # Update world map
            self.world_map.update_current_chunk(chunk_x, chunk_y)
            
            # Update areas
            for area in self.areas.values():
                area.update()
                
            # Optionally, use camera for effects or chunk loading
            # (currently not used, but available for future features)
            
        except Exception as e:
            raise WorldError(f"Failed to update world: {str(e)}")
    
    def draw(self, screen, camera):
        """Draw the world"""
        try:
            # Calculate visible chunks
            start_x = max(0, int(camera.x // self.chunk_size) - 1)
            start_y = max(0, int(camera.y // self.chunk_size) - 1)
            end_x = min(self.width // self.chunk_size, int((camera.x + screen.get_width()) // self.chunk_size) + 1)
            end_y = min(self.height // self.chunk_size, int((camera.y + screen.get_height()) // self.chunk_size) + 1)
            
            # Draw visible chunks
            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    chunk = self.get_chunk(x, y)
                    chunk.draw(screen, camera)
                    
            # Draw gates
            for gate in self.gates.values():
                gate.draw(screen, camera)
                
        except Exception as e:
            raise WorldError(f"Failed to draw world: {str(e)}")
    
    def add_gate(self, x, y, gate_type, target_x, target_y):
        """Add a gate to the world"""
        try:
            gate_key = (x, y)
            if gate_key in self.gates:
                raise WorldError(f"Gate already exists at ({x}, {y})")
                
            self.gates[gate_key] = GateType(x, y, gate_type, target_x, target_y)
            
        except Exception as e:
            raise WorldError(f"Failed to add gate: {str(e)}")
    
    def to_dict(self):
        """Convert world state to dictionary"""
        try:
            return {
                'areas': {f"{x},{y}": area.to_dict() for (x, y), area in self.areas.items()},
                'gates': {f"{x},{y}": gate.to_dict() for (x, y), gate in self.gates.items()},
                'visited_chunks': [f"{x},{y}" for x, y in self.visited_chunks]
            }
        except Exception as e:
            raise WorldError(f"Failed to serialize world: {str(e)}")
    
    def from_dict(self, data):
        """Load world state from dictionary"""
        try:
            # Clear existing state
            self.areas.clear()
            self.gates.clear()
            self.visited_chunks.clear()
            
            # Load areas
            for key, area_data in data['areas'].items():
                x, y = map(int, key.split(','))
                area = Area(x, y, self.chunk_size)
                area.from_dict(area_data)
                self.areas[(x, y)] = area
                
            # Load gates
            for key, gate_data in data['gates'].items():
                x, y = map(int, key.split(','))
                gate = GateType(x, y, gate_data['type'], gate_data['target_x'], gate_data['target_y'])
                self.gates[(x, y)] = gate
                
            # Load visited chunks
            self.visited_chunks = {tuple(map(int, key.split(','))) for key in data['visited_chunks']}
            
        except Exception as e:
            raise WorldError(f"Failed to deserialize world: {str(e)}")

    def generate_chunk(self, chunk_x, chunk_y):
        """Generate a new chunk at the given coordinates and return its tile data as a 2D array of tile types."""
        chunk = Chunk(chunk_x, chunk_y, self.chunk_size)
        chunk.generate()
        # Return just the tile type 2D array for compatibility with the rest of the code
        return chunk.tiles