import pygame
import random
import noise
from enum import Enum

class AreaType(Enum):
    FOREST = "forest"
    CAVE = "cave"
    DUNGEON = "dungeon"
    VILLAGE = "village"

class GateType(Enum):
    NONE = "none"
    KEY = "key"
    BOSS = "boss"
    HIDDEN = "hidden"
    DESTRUCTIBLE = "destructible"

class Gate:
    def __init__(self, x, y, gate_type, required_item=None, health=100):
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.required_item = required_item
        self.health = health
        self.max_health = health
        self.is_open = False
        self.is_hidden = gate_type == GateType.HIDDEN
        self.is_destroyed = False
        
        # Create gate surface
        self.width = 64
        self.height = 96
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_gate()
    
    def _draw_gate(self):
        if self.is_hidden:
            # Draw hidden gate as a wall
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height))
            pygame.draw.rect(self.surface, (150, 150, 150), (0, 0, self.width, self.height), 2)
        elif self.is_destroyed:
            # Draw destroyed gate
            pygame.draw.rect(self.surface, (50, 50, 50), (0, 0, self.width, self.height))
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 2)
        else:
            # Draw normal gate
            gate_color = (150, 100, 50) if self.gate_type == GateType.KEY else (100, 100, 150)
            pygame.draw.rect(self.surface, gate_color, (0, 0, self.width, self.height))
            pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.width, self.height), 2)
            
            # Draw lock if key is required
            if self.gate_type == GateType.KEY:
                pygame.draw.circle(self.surface, (200, 200, 50), (self.width//2, self.height//2), 10)
                pygame.draw.circle(self.surface, (150, 150, 50), (self.width//2, self.height//2), 10, 2)
    
    def can_open(self, player):
        if self.is_open or self.is_destroyed:
            return True
        if self.gate_type == GateType.KEY:
            return self.required_item in player.inventory
        return False
    
    def open(self):
        if not self.is_open and not self.is_destroyed:
            self.is_open = True
            self._draw_gate()
    
    def damage(self, amount):
        if self.gate_type == GateType.DESTRUCTIBLE and not self.is_destroyed:
            self.health -= amount
            if self.health <= 0:
                self.is_destroyed = True
                self._draw_gate()
            return True
        return False
    
    def reveal(self):
        if self.is_hidden:
            self.is_hidden = False
            self._draw_gate()
    
    def draw(self, screen, camera):
        if not self.is_hidden:
            screen_x, screen_y = camera.apply(self)
            screen.blit(self.surface, (screen_x, screen_y))
            
            # Draw health bar for destructible gates
            if self.gate_type == GateType.DESTRUCTIBLE and not self.is_destroyed:
                health_width = 40
                health_height = 4
                health_x = screen_x + (self.width - health_width) // 2
                health_y = screen_y - 10
                
                # Background
                pygame.draw.rect(screen, (100, 100, 100), 
                               (health_x, health_y, health_width, health_height))
                # Health
                health_percent = self.health / self.max_health
                pygame.draw.rect(screen, (255, 100, 100), 
                               (health_x, health_y, 
                                int(health_width * health_percent), health_height))

class Area:
    def __init__(self, area_type, seed=None):
        self.area_type = area_type
        self.seed = seed or random.randint(0, 1000000)
        self.gates = []
        self.visited = False
        self.cleared = False
        
        # Area-specific generation parameters
        self.parameters = {
            AreaType.FOREST: {
                'scale': 50.0,
                'octaves': 6,
                'persistence': 0.5,
                'lacunarity': 2.0,
                'water_threshold': 0.3,
                'sand_threshold': 0.4
            },
            AreaType.CAVE: {
                'scale': 30.0,
                'octaves': 4,
                'persistence': 0.6,
                'lacunarity': 2.5,
                'water_threshold': 0.2,
                'sand_threshold': 0.3
            },
            AreaType.DUNGEON: {
                'scale': 20.0,
                'octaves': 3,
                'persistence': 0.7,
                'lacunarity': 3.0,
                'water_threshold': 0.1,
                'sand_threshold': 0.2
            },
            AreaType.VILLAGE: {
                'scale': 40.0,
                'octaves': 5,
                'persistence': 0.4,
                'lacunarity': 1.8,
                'water_threshold': 0.25,
                'sand_threshold': 0.35
            }
        }
    
    def generate_gates(self, chunk_size, world_width, world_height):
        """Generate gates for this area"""
        params = self.parameters[self.area_type]
        
        # Generate main gates
        if self.area_type == AreaType.FOREST:
            # Forest has key gates to cave and dungeon
            self.gates.append(Gate(
                world_width // 4,
                world_height // 2,
                GateType.KEY,
                "cave_key"
            ))
            self.gates.append(Gate(
                3 * world_width // 4,
                world_height // 2,
                GateType.KEY,
                "dungeon_key"
            ))
        elif self.area_type == AreaType.CAVE:
            # Cave has a boss gate and hidden passages
            self.gates.append(Gate(
                world_width // 2,
                world_height // 2,
                GateType.BOSS
            ))
            # Add some hidden passages
            for _ in range(3):
                x = random.randint(0, world_width)
                y = random.randint(0, world_height)
                self.gates.append(Gate(x, y, GateType.HIDDEN))
        elif self.area_type == AreaType.DUNGEON:
            # Dungeon has destructible walls and key gates
            for _ in range(5):
                x = random.randint(0, world_width)
                y = random.randint(0, world_height)
                self.gates.append(Gate(x, y, GateType.DESTRUCTIBLE))
            
            self.gates.append(Gate(
                world_width // 2,
                world_height // 2,
                GateType.KEY,
                "boss_key"
            ))
    
    def get_tile_type(self, x, y):
        """Get tile type based on area type and position"""
        params = self.parameters[self.area_type]
        
        # Generate noise value for this position
        nx = x / params['scale']
        ny = y / params['scale']
        elevation = noise.pnoise2(nx, ny, 
                                octaves=params['octaves'], 
                                persistence=params['persistence'], 
                                lacunarity=params['lacunarity'], 
                                repeatx=1024, 
                                repeaty=1024, 
                                base=self.seed)
        
        # Normalize elevation to 0-1 range
        elevation = (elevation + 1) / 2
        
        # Determine tile type based on elevation and area type
        if elevation < params['water_threshold']:
            return 'water'
        elif elevation < params['sand_threshold']:
            return 'sand'
        else:
            if self.area_type == AreaType.FOREST:
                return 'grass'
            elif self.area_type == AreaType.CAVE:
                return 'stone'
            elif self.area_type == AreaType.DUNGEON:
                return 'brick'
            else:  # VILLAGE
                return 'path'
    
    def to_dict(self):
        """Convert area data to dictionary for saving"""
        return {
            'type': self.area_type.value,
            'seed': self.seed,
            'visited': self.visited,
            'cleared': self.cleared,
            'gates': [{
                'x': gate.x,
                'y': gate.y,
                'type': gate.gate_type.value,
                'required_item': gate.required_item,
                'health': gate.health,
                'is_open': gate.is_open,
                'is_hidden': gate.is_hidden,
                'is_destroyed': gate.is_destroyed
            } for gate in self.gates]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create area from saved data"""
        area = cls(AreaType(data['type']), data['seed'])
        area.visited = data['visited']
        area.cleared = data['cleared']
        
        # Recreate gates
        for gate_data in data['gates']:
            gate = Gate(
                gate_data['x'],
                gate_data['y'],
                GateType(gate_data['type']),
                gate_data['required_item'],
                gate_data['health']
            )
            gate.is_open = gate_data['is_open']
            gate.is_hidden = gate_data['is_hidden']
            gate.is_destroyed = gate_data['is_destroyed']
            gate._draw_gate()
            area.gates.append(gate)
        
        return area 