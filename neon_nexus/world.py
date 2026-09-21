# world.py
import random
import pygame
from collections import defaultdict
import noise
import math
from areas import Area, AreaType, GateType, Gate
from world_map import WorldMap
from portal import Portal
from environment import Box, Lever, PressurePlate, DestructibleBlock
from enemy import Enemy, Boss
from error_handler import WorldError

class Tile:
    def __init__(self, name, is_solid=False):
        self.name = name
        self.is_solid = is_solid

class Chunk:
    def __init__(self, x, y, size=32):
        self.x = x
        self.y = y
        self.size = size
        self.tiles = [[None for _ in range(size)] for _ in range(size)]
        self.generated = False
        self.entities = []
        self.generate()
    
    def generate(self, seed=None):
        if self.generated:
            return
            
        if seed is not None:
            random.seed(seed + self.x * 1000 + self.y)
            
        # Generate terrain for this chunk
        for y in range(self.size):
            for x in range(self.size):
                self.tiles[y][x] = 'grass'
                if random.random() < 0.02:
                    self.tiles[y][x] = 'water'
                elif random.random() < 0.01:
                    self.tiles[y][x] = 'mountain'
                    
        self._smooth_edges()
        self.generated = True
    
    def _smooth_edges(self):
        for y in range(self.size):
            for x in range(self.size):
                if x == 0 or y == 0 or x == self.size - 1 or y == self.size - 1:
                    if self.tiles[y][x] == 'water':
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                nx, ny = x + dx, y + dy
                                if (0 <= nx < self.size and 0 <= ny < self.size and 
                                    self.tiles[ny][nx] == 'grass'):
                                    self.tiles[ny][nx] = 'sand'

    def get_tile(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            tile_name = self.tiles[y][x] or 'grass'
            is_solid = tile_name in ('mountain', 'water')
            return Tile(tile_name, is_solid=is_solid)
        return None

    def draw(self, screen, camera, tile_images=None, chunk_size=32):
        screen_x = self.x * chunk_size - camera.x
        screen_y = self.y * chunk_size - camera.y
        
        if tile_images:
            tile_type = self.tiles[0][0] if self.tiles and self.tiles[0] else 'grass'
            img = tile_images.get(tile_type, tile_images.get('grass'))
            if img:
                screen.blit(img, (screen_x, screen_y))
                return

        color = (100, 200, 100)
        pygame.draw.rect(screen, color, (screen_x, screen_y, chunk_size, chunk_size))

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'size': self.size,
            'tiles': self.tiles,
            'generated': self.generated
        }

class World:
    def __init__(self, width, height, chunk_size):
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.chunks = {}
        self.areas = {}
        self.gates = {}
        self.visited_chunks = set()
        self.world_map = WorldMap(width, height, chunk_size)
        self.portals = []
        self.boxes = []
        self.levers = []
        self.plates = []
        self.destructibles = []
        self.enemies = []
        self.bosses = []

        # Default portals
        self.portals.append(Portal(0, 0, self.chunk_size // 2, self.chunk_size // 2, name="Spawn Portal"))
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
            'path': pygame.Surface((self.chunk_size, self.chunk_size)),
            'mountain': pygame.Surface((self.chunk_size, self.chunk_size))
        }
        self.tile_images['grass'].fill((100, 200, 100))
        self.tile_images['water'].fill((100, 100, 255))
        self.tile_images['sand'].fill((200, 200, 100))
        self.tile_images['stone'].fill((150, 150, 150))
        self.tile_images['brick'].fill((200, 100, 100))
        self.tile_images['path'].fill((200, 200, 200))
        self.tile_images['mountain'].fill((120, 120, 120))
    
    def get_chunk(self, x, y):
        """Get or create a chunk at the specified coordinates"""
        try:
            chunk_key = (x, y)
            if chunk_key not in self.chunks:
                self.chunks[chunk_key] = Chunk(x, y, self.chunk_size)
            return self.chunks[chunk_key]
        except Exception as e:
            raise WorldError(f"Failed to get chunk at ({x}, {y}): {str(e)}")
    
    def update(self, camera, player):
        """Update world state"""
        try:
            chunk_x = int(player.x // self.chunk_size)
            chunk_y = int(player.y // self.chunk_size)
            self.visited_chunks.add((chunk_x, chunk_y))
            
            self.world_map.update_current_chunk(chunk_x, chunk_y)
            
            for area in self.areas.values():
                area.update()
                
            for box in self.boxes:
                box.update()
            for plate in self.plates:
                plate.update(player)
            for enemy in self.enemies:
                enemy.update(player)
            for boss in self.bosses:
                boss.update(player)
                
        except Exception as e:
            raise WorldError(f"Failed to update world: {str(e)}")
    
    def draw(self, screen, camera):
        """Draw the world"""
        try:
            start_x = max(0, int(camera.x // self.chunk_size) - 1)
            start_y = max(0, int(camera.y // self.chunk_size) - 1)
            end_x = min(self.width // self.chunk_size, int((camera.x + screen.get_width()) // self.chunk_size) + 1)
            end_y = min(self.height // self.chunk_size, int((camera.y + screen.get_height()) // self.chunk_size) + 1)
            
            for x in range(start_x, end_x + 1):
                for y in range(start_y, end_y + 1):
                    chunk = self.get_chunk(x, y)
                    chunk.draw(screen, camera, self.tile_images, self.chunk_size)
                    
            for gate in self.gates.values():
                gate.draw(screen, camera)
            
            for portal in self.portals:
                portal.draw(screen, camera, self.chunk_size)
                
            for box in self.boxes:
                box.draw(screen, camera)
            for lever in self.levers:
                lever.draw(screen, camera)
            for plate in self.plates:
                plate.draw(screen, camera)
            for destructible in self.destructibles:
                destructible.draw(screen, camera)
            for enemy in self.enemies:
                enemy.draw(screen, camera)
            for boss in self.bosses:
                boss.draw(screen, camera)
                
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
                'chunks': {f"{x},{y}": chunk.to_dict() for (x, y), chunk in self.chunks.items()},
                'areas': {area_type.value: area.to_dict() for area_type, area in self.areas.items()},
                'gates': {f"{x},{y}": gate.to_dict() if hasattr(gate, 'to_dict') else str(gate) for (x, y), gate in self.gates.items()},
                'visited_chunks': [f"{x},{y}" for x, y in self.visited_chunks]
            }
        except Exception as e:
            raise WorldError(f"Failed to serialize world: {str(e)}")
    
    def from_dict(self, data):
        """Load world state from dictionary"""
        try:
            self.chunks.clear()
            self.areas.clear()
            self.gates.clear()
            self.visited_chunks.clear()
            
            for key, area_data in data.get('areas', {}).items():
                try:
                    area_type = AreaType(key)
                    area = Area.from_dict(area_data)
                    self.areas[area_type] = area
                except Exception:
                    pass
                
            for key, chunk_data in data.get('chunks', {}).items():
                try:
                    x, y = map(int, key.split(','))
                    chunk = Chunk(x, y, self.chunk_size)
                    if isinstance(chunk_data, dict) and 'tiles' in chunk_data:
                        chunk.tiles = chunk_data['tiles']
                        chunk.generated = True
                    self.chunks[(x, y)] = chunk
                except Exception:
                    pass

            for key in data.get('visited_chunks', []):
                try:
                    x, y = map(int, key.split(','))
                    self.visited_chunks.add((x, y))
                except Exception:
                    pass
            
            return self
            
        except Exception as e:
            raise WorldError(f"Failed to deserialize world: {str(e)}")

    def generate_chunk(self, chunk_x, chunk_y):
        chunk = self.get_chunk(chunk_x, chunk_y)
        return chunk.tiles