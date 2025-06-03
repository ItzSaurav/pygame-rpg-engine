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
    def __init__(self):
        self.chunk_size = 32
        self.world_width = 100 * self.chunk_size
        self.world_height = 100 * self.chunk_size
        self.chunks = {}
        self.areas = {}
        self.gates = []
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
                self.world_width,
                self.world_height
            )
        # Create world map
        self.world_map = WorldMap(self.world_width, self.world_height, self.chunk_size)
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
        """Get or generate a chunk at the specified coordinates"""
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        chunk_key = (chunk_x, chunk_y)
        
        if chunk_key not in self.chunks:
            self.chunks[chunk_key] = self.generate_chunk(chunk_x, chunk_y)
            # Mark chunk as visited on the map
            self.world_map.mark_chunk_visited(chunk_x, chunk_y)
        
        return self.chunks[chunk_key]
    
    def update(self, camera, player=None):
        """Update world state"""
        # Update current chunk on map
        visible_rect = camera.get_visible_rect()
        self.world_map.update_current_chunk(visible_rect.x, visible_rect.y)
        
        # Update map
        self.world_map.update()
        
        # Update visible chunks
        visible_chunks = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                chunk_x = int(visible_rect.x // self.chunk_size) + x
                chunk_y = int(visible_rect.y // self.chunk_size) + y
                self.get_chunk(chunk_x * self.chunk_size, chunk_y * self.chunk_size)
                visible_chunks.add((chunk_x, chunk_y))
        
        # Remove chunks that are too far away
        for chunk_key in list(self.chunks.keys()):
            if chunk_key not in visible_chunks:
                del self.chunks[chunk_key]
        
        # Check for player proximity to portals
        if player:
            player_chunk_x = int(player.x // self.chunk_size)
            player_chunk_y = int(player.y // self.chunk_size)
            for portal in self.portals:
                if portal.chunk_x == player_chunk_x and portal.chunk_y == player_chunk_y:
                    # Calculate distance from player to portal
                    dx = player.x - (portal.chunk_x * self.chunk_size + portal.x)
                    dy = player.y - (portal.chunk_y * self.chunk_size + portal.y)
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance < 50:  # Unlock if player is within 50 pixels
                        portal.unlocked = True
        
        # Update environmental objects
        for box in self.boxes:
            box.update()
        for plate in self.plates:
            plate.update(player)
        for enemy in self.enemies:
            enemy.update(player)
        for boss in self.bosses:
            boss.update(player)
    
    def draw(self, screen, camera):
        """Draw the world"""
        # Draw chunks
        for chunk_key, chunk in self.chunks.items():
            chunk_x, chunk_y = chunk_key
            screen_x = chunk_x * self.chunk_size - camera.x
            screen_y = chunk_y * self.chunk_size - camera.y
            
            # Draw tiles
            for y in range(self.chunk_size):
                for x in range(self.chunk_size):
                    tile = chunk[y][x]
                    if tile:
                        # Use the correct tile image
                        tile_img = self.tile_images.get(tile)
                        if tile_img:
                            screen.blit(tile_img, (screen_x + x, screen_y + y))
                        else:
                            # fallback: draw a magenta pixel for unknown tile types
                            pygame.draw.rect(screen, (255, 0, 255), (screen_x + x, screen_y + y, 1, 1))
        
        # Draw portals
        for portal in self.portals:
            portal.draw(screen, camera, self.chunk_size)
        
        # Draw map
        self.world_map.draw(screen)
        
        # Draw environmental objects
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
    
    def to_dict(self):
        """Convert world data to dictionary for saving"""
        return {
            'chunks': {str(k): v for k, v in self.chunks.items()},
            'areas': {area_type.name: area.to_dict() for area_type, area in self.areas.items()},
            'gates': [gate.to_dict() for gate in self.gates],
            'world_map': self.world_map.to_dict(),
            'portals': [portal.to_dict() for portal in self.portals],
            'boxes': [box.to_dict() for box in self.boxes],
            'levers': [lever.to_dict() for lever in self.levers],
            'plates': [plate.to_dict() for plate in self.plates],
            'destructibles': [destructible.to_dict() for destructible in self.destructibles],
            'enemies': [enemy.to_dict() for enemy in self.enemies],
            'bosses': [boss.to_dict() for boss in self.bosses]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create world from saved data"""
        world = cls()
        world.chunks = {eval(k): v for k, v in data['chunks'].items()}
        world.areas = {AreaType[area_type]: Area.from_dict(area_data) 
                      for area_type, area_data in data['areas'].items()}
        world.gates = [Gate.from_dict(gate_data) for gate_data in data['gates']]
        world.world_map = WorldMap.from_dict(data['world_map'], 
                                           world.world_width, 
                                           world.world_height, 
                                           world.chunk_size)
        world.portals = [Portal.from_dict(portal_data) for portal_data in data.get('portals', [])]
        world.boxes = [Box.from_dict(box_data) for box_data in data.get('boxes', [])]
        world.levers = [Lever.from_dict(lever_data) for lever_data in data.get('levers', [])]
        world.plates = [PressurePlate.from_dict(plate_data) for plate_data in data.get('plates', [])]
        world.destructibles = [DestructibleBlock.from_dict(destructible_data) for destructible_data in data.get('destructibles', [])]
        world.enemies = [Enemy.from_dict(enemy_data) for enemy_data in data.get('enemies', [])]
        world.bosses = [Boss.from_dict(boss_data) for boss_data in data.get('bosses', [])]
        return world

    def generate_chunk(self, chunk_x, chunk_y):
        """Generate a new chunk at the given coordinates and return its tile data as a 2D array of tile types."""
        chunk = Chunk(chunk_x, chunk_y, self.chunk_size)
        chunk.generate()
        # Return just the tile type 2D array for compatibility with the rest of the code
        return chunk.tiles