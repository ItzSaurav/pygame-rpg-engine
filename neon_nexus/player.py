# player.py
import pygame
from collections import defaultdict
import math
import random
from projectile import Projectile
from error_handler import StateError, InputError

class Item:
    def __init__(self, name, description, image=None):
        self.name = name
        self.description = description
        self.image = image or pygame.Surface((32, 32))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.speed = 5
        self.jump_power = 15
        self.super_jump_power = 25
        self.gravity = 0.8
        self.velocity_y = 0
        self.on_ground = False
        self.jumping = False
        self.jump_hold_time = 0
        self.max_jump_hold = 20
        self.landing_timer = 0
        self.landing_duration = 10
        self.max_fall_speed = 20
        self.ground_y = 400
        
        # Combat attributes
        self.health = 100
        self.max_health = 100
        self.attack_power = 20
        self.attack_cooldown = 0
        self.attack_cooldown_time = 30
        self.attack_charge = 0
        self.max_attack_charge = 60
        self.attack_range = 50
        
        # Magic attributes
        self.mana = 100
        self.max_mana = 100
        self.mana_regen = 0.5
        self.spell_cooldown = 0
        self.spell_cooldown_time = 45
        self.spell_power = 15
        self.spell_range = 300
        self.spell_speed = 10
        self.current_spell = "fire"  # fire, ice, lightning
        self.spell_levels = {
            "fire": 1,
            "ice": 1,
            "lightning": 1
        }
        self.projectiles = []
        
        # Progression
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.inventory = {}
        self.selected_item = None
        
        # Area interaction
        self.interaction_range = 50
        self.interaction_cooldown = 0
        self.interaction_cooldown_time = 20
        
        # Create player surface
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_player()
        
        # Base stats
        self.base_speed = 5
        self.base_health = 100
        self.base_mana = 100
        
        # Current stats
        self.speed = self.base_speed
        self.health = self.base_health
        self.max_health = self.base_health
        self.mana = self.base_mana
        self.max_mana = self.base_mana
        
        # Stat growth per level
        self.speed_growth = 0.5
        self.health_growth = 20
        self.mana_growth = 15
        
        # Level-up effect
        self.level_up_effect = {
            'active': False,
            'duration': 60,  # Frames
            'current_frame': 0,
            'particles': []
        }
    
    def _draw_player(self):
        # Clear surface
        self.surface.fill((0, 0, 0, 0))
        
        # Draw body (muscular, tan)
        body_color = (220, 180, 120)
        pygame.draw.rect(self.surface, body_color, (8, 16, 16, 28), border_radius=6)
        
        # Draw green haramaki (belt)
        haramaki_color = (40, 180, 40)
        pygame.draw.rect(self.surface, haramaki_color, (8, 32, 16, 8), border_radius=3)
        
        # Draw head (tan)
        pygame.draw.ellipse(self.surface, body_color, (8, 0, 16, 18))
        
        # Draw green hair (spiky)
        hair_color = (60, 200, 60)
        pygame.draw.ellipse(self.surface, hair_color, (8, -4, 16, 10))
        pygame.draw.polygon(self.surface, hair_color, [(16, 0), (12, -6), (20, -6)])
        pygame.draw.polygon(self.surface, hair_color, [(12, 2), (8, -2), (14, -4)])
        pygame.draw.polygon(self.surface, hair_color, [(20, 2), (24, -2), (18, -4)])
        
        # Draw eyes (serious look)
        pygame.draw.rect(self.surface, (0, 0, 0), (13, 7, 3, 2))
        pygame.draw.rect(self.surface, (0, 0, 0), (18, 7, 3, 2))
        
        # Draw mouth sword (horizontal line, white blade, black hilt)
        pygame.draw.line(self.surface, (255, 255, 255), (8, 14), (24, 14), 2)
        pygame.draw.rect(self.surface, (0, 0, 0), (7, 13, 2, 4))
        pygame.draw.rect(self.surface, (0, 0, 0), (23, 13, 2, 4))
        
        # Draw left sword (at side, angled)
        pygame.draw.line(self.surface, (255, 255, 255), (6, 38), (2, 48), 2)
        pygame.draw.rect(self.surface, (0, 0, 0), (1, 47, 4, 2))
        
        # Draw right sword (at side, angled)
        pygame.draw.line(self.surface, (255, 255, 255), (26, 38), (30, 48), 2)
        pygame.draw.rect(self.surface, (0, 0, 0), (29, 47, 4, 2))
        
        # Draw boots
        pygame.draw.rect(self.surface, (60, 60, 60), (10, 44, 4, 4))
        pygame.draw.rect(self.surface, (60, 60, 60), (18, 44, 4, 4))
        
        # Draw magic aura if casting
        if self.spell_cooldown > self.spell_cooldown_time - 10:
            aura_color = {
                "fire": (255, 100, 0, 100),
                "ice": (100, 200, 255, 100),
                "lightning": (255, 255, 100, 100)
            }[self.current_spell]
            aura = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            pygame.draw.circle(aura, aura_color, (self.width//2 + 10, self.height//2 + 10), 20)
            self.surface.blit(aura, (-10, -10), special_flags=pygame.BLEND_RGBA_ADD)
    
    def move(self, dx, dy):
        # Update position
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Keep player in bounds
        self.x = max(0, min(self.x, 800 - self.width))
        self.y = max(0, min(self.y, 600 - self.height))
        
        # Update player appearance
        self._draw_player()
    
    def jump(self):
        if self.on_ground and not self.jumping:
            self.jumping = True
            self.jump_hold_time = 0
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self._draw_player()
    
    def update_jump(self):
        if self.jumping:
            # Apply gravity
            self.velocity_y = min(self.velocity_y + self.gravity, self.max_fall_speed)
            self.y += self.velocity_y
            
            # Check for landing
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.velocity_y = 0
                self.jumping = False
                self.on_ground = True
                self.landing_timer = self.landing_duration
                self._draw_player()
        
        # Update landing timer
        if self.landing_timer > 0:
            self.landing_timer -= 1
    
    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_time
            self.attack_charge = 0
            return True
        return False
    
    def interact(self, world):
        """Interact with nearby objects (gates, items, etc.)"""
        if self.interaction_cooldown > 0:
            return
        
        # Check for gates in interaction range
        gate = world.get_gate_at(self.x + self.width//2, self.y + self.height//2)
        if gate:
            if gate.can_open(self):
                gate.open()
            elif gate.gate_type == 'destructible':
                gate.damage(self.attack_power)
            elif gate.gate_type == 'hidden':
                gate.reveal()
        
        self.interaction_cooldown = self.interaction_cooldown_time
    
    def cast_spell(self, target_x, target_y):
        """Cast a spell at the target position"""
        if self.spell_cooldown <= 0 and self.mana >= 20:
            # Create projectile
            projectile = Projectile(
                self.x + self.width//2,
                self.y + self.height//2,
                target_x,
                target_y,
                self.spell_speed,
                self.spell_power * self.spell_levels[self.current_spell],
                self.current_spell
            )
            self.projectiles.append(projectile)
            
            # Apply costs
            self.spell_cooldown = self.spell_cooldown_time
            self.mana -= 20
            
            # Update appearance
            self._draw_player()
            return True
        return False
    
    def switch_spell(self, spell_type):
        """Switch to a different spell type"""
        if spell_type in self.spell_levels:
            self.current_spell = spell_type
            self._draw_player()
    
    def upgrade_spell(self, spell_type):
        """Upgrade a spell type"""
        if spell_type in self.spell_levels and self.spell_levels[spell_type] < 3:
            self.spell_levels[spell_type] += 1
            return True
        return False
    
    def add_xp(self, amount):
        """Add experience points and handle level-up"""
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Handle level-up effects and stat increases"""
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # Increase XP needed for next level
        
        # Increase stats
        self.speed = self.base_speed + (self.level - 1) * self.speed_growth
        self.max_health = self.base_health + (self.level - 1) * self.health_growth
        self.max_mana = self.base_mana + (self.level - 1) * self.mana_growth
        
        # Restore health and mana
        self.health = self.max_health
        self.mana = self.max_mana
        
        # Activate level-up effect
        self.level_up_effect['active'] = True
        self.level_up_effect['current_frame'] = 0
        self.level_up_effect['particles'] = []
        
        # Generate particles for level-up effect
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            self.level_up_effect['particles'].append({
                'x': self.width // 2,
                'y': self.height // 2,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': random.randint(30, 60)
            })
    
    def update_level_up_effect(self):
        """Update level-up visual effect"""
        if not self.level_up_effect['active']:
            return
        
        self.level_up_effect['current_frame'] += 1
        
        # Update particles
        for particle in self.level_up_effect['particles'][:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.level_up_effect['particles'].remove(particle)
        
        # End effect if duration is over
        if self.level_up_effect['current_frame'] >= self.level_up_effect['duration']:
            self.level_up_effect['active'] = False
    
    def draw_level_up_effect(self, screen, camera):
        """Draw level-up visual effect"""
        if not self.level_up_effect['active']:
            return
        
        # Calculate screen position
        screen_x, screen_y = camera.apply(self)
        
        # Draw particles
        for particle in self.level_up_effect['particles']:
            alpha = int(255 * (particle['life'] / 60))
            color = (255, 255, 100, alpha)
            pos = (screen_x + particle['x'], screen_y + particle['y'])
            pygame.draw.circle(screen, color, pos, 3)
        
        # Draw level-up text
        if self.level_up_effect['current_frame'] < 30:  # Show text for first half of effect
            text = pygame.font.Font(None, 36).render(f"Level {self.level}!", True, (255, 255, 100))
            text_pos = (screen_x + self.width//2 - text.get_width()//2, 
                       screen_y - 30 - self.level_up_effect['current_frame'])
            screen.blit(text, text_pos)
    
    def update(self, world):
        """Update player state"""
        try:
            # Apply gravity
            self.velocity_y += self.gravity
            
            # Update position
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Check collisions
            self._handle_collisions(world)
            
            # Update cooldowns
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            if self.spell_cooldown > 0:
                self.spell_cooldown -= 1
                
            # Regenerate mana
            if self.mana < self.max_mana:
                self.mana = min(self.max_mana, self.mana + self.mana_regen)
                
        except Exception as e:
            raise StateError(f"Failed to update player: {str(e)}")
            
    def _handle_collisions(self, world):
        """Handle collisions with world objects"""
        try:
            # Get current chunk
            chunk_x = int(self.x // world.chunk_size)
            chunk_y = int(self.y // world.chunk_size)
            chunk = world.get_chunk(chunk_x, chunk_y)
            
            # Check tile collisions
            tile_x = int(self.x % world.chunk_size)
            tile_y = int(self.y % world.chunk_size)
            
            # Check surrounding tiles
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    check_x = tile_x + dx
                    check_y = tile_y + dy
                    
                    if 0 <= check_x < world.chunk_size and 0 <= check_y < world.chunk_size:
                        tile = chunk.get_tile(check_x, check_y)
                        if tile and tile.is_solid:
                            self._resolve_collision(tile, check_x, check_y)
                            
        except Exception as e:
            raise StateError(f"Failed to handle collisions: {str(e)}")
            
    def _resolve_collision(self, tile, tile_x, tile_y):
        """Resolve collision with a tile"""
        try:
            # Calculate collision rectangle
            tile_rect = pygame.Rect(tile_x, tile_y, 1, 1)
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            
            if player_rect.colliderect(tile_rect):
                # Calculate overlap
                overlap_x = min(player_rect.right - tile_rect.left, tile_rect.right - player_rect.left)
                overlap_y = min(player_rect.bottom - tile_rect.top, tile_rect.bottom - player_rect.top)
                
                # Resolve collision
                if overlap_x < overlap_y:
                    if player_rect.centerx < tile_rect.centerx:
                        self.x = tile_rect.left - player_rect.width
                    else:
                        self.x = tile_rect.right
                    self.velocity_x = 0
                else:
                    if player_rect.centery < tile_rect.centery:
                        self.y = tile_rect.top - player_rect.height
                        self.velocity_y = 0
                        self.on_ground = True
                    else:
                        self.y = tile_rect.bottom
                        self.velocity_y = 0
                        
        except Exception as e:
            raise StateError(f"Failed to resolve collision: {str(e)}")
            
    def move(self, direction):
        """Move the player"""
        try:
            if direction == 'left':
                self.velocity_x = -self.speed
            elif direction == 'right':
                self.velocity_x = self.speed
            else:
                self.velocity_x = 0
                
        except Exception as e:
            raise InputError(f"Failed to move player: {str(e)}")
            
    def jump(self):
        """Make the player jump"""
        try:
            if self.on_ground:
                self.velocity_y = self.jump_power
                self.on_ground = False
                
        except Exception as e:
            raise InputError(f"Failed to make player jump: {str(e)}")
            
    def attack(self):
        """Perform an attack"""
        try:
            if self.attack_cooldown <= 0:
                # TODO: Implement attack logic
                self.attack_cooldown = 30
                
        except Exception as e:
            raise InputError(f"Failed to perform attack: {str(e)}")
            
    def cast_spell(self, spell_name):
        """Cast a spell"""
        try:
            if spell_name not in self.spells:
                raise InputError(f"Unknown spell: {spell_name}")
                
            spell = self.spells[spell_name]
            if self.spell_cooldown <= 0 and self.mana >= spell['mana_cost']:
                # TODO: Implement spell casting logic
                self.mana -= spell['mana_cost']
                self.spell_cooldown = spell['cooldown']
                
        except Exception as e:
            raise InputError(f"Failed to cast spell: {str(e)}")
            
    def take_damage(self, amount):
        """Take damage"""
        try:
            self.health = max(0, self.health - amount)
            return self.health <= 0
            
        except Exception as e:
            raise StateError(f"Failed to take damage: {str(e)}")
            
    def heal(self, amount):
        """Heal the player"""
        try:
            self.health = min(self.max_health, self.health + amount)
            
        except Exception as e:
            raise StateError(f"Failed to heal player: {str(e)}")
            
    def gain_xp(self, amount):
        """Gain experience points"""
        try:
            self.xp += amount
            while self.xp >= self.xp_to_next_level:
                self.level_up()
                
        except Exception as e:
            raise StateError(f"Failed to gain XP: {str(e)}")
            
    def level_up(self):
        """Level up the player"""
        try:
            self.level += 1
            self.xp -= self.xp_to_next_level
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            
            # Increase stats
            self.max_health += 10
            self.health = self.max_health
            self.max_mana += 5
            self.mana = self.max_mana
            self.speed += 0.2
            
        except Exception as e:
            raise StateError(f"Failed to level up: {str(e)}")
            
    def draw(self, screen, camera):
        """Draw the player"""
        try:
            # Draw player sprite
            screen_x = self.x - camera.x
            screen_y = self.y - camera.y
            
            # Draw body
            pygame.draw.rect(screen, (210, 180, 140), (screen_x, screen_y, self.width, self.height))
            
            # Draw green haramaki
            pygame.draw.rect(screen, (0, 255, 0), (screen_x + 8, screen_y + 20, self.width - 16, 20))
            
            # Draw swords
            sword_color = (200, 200, 200)
            if self.velocity_x > 0:
                pygame.draw.line(screen, sword_color, (screen_x + self.width, screen_y + 10), 
                               (screen_x + self.width + 20, screen_y + 10), 2)
                pygame.draw.line(screen, sword_color, (screen_x + self.width, screen_y + 20), 
                               (screen_x + self.width + 25, screen_y + 20), 2)
                pygame.draw.line(screen, sword_color, (screen_x + self.width, screen_y + 30), 
                               (screen_x + self.width + 15, screen_y + 30), 2)
            else:
                pygame.draw.line(screen, sword_color, (screen_x, screen_y + 10), 
                               (screen_x - 20, screen_y + 10), 2)
                pygame.draw.line(screen, sword_color, (screen_x, screen_y + 20), 
                               (screen_x - 25, screen_y + 20), 2)
                pygame.draw.line(screen, sword_color, (screen_x, screen_y + 30), 
                               (screen_x - 15, screen_y + 30), 2)
            
            # Draw health bar
            health_width = (self.width * self.health) // self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (screen_x, screen_y - 10, self.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (screen_x, screen_y - 10, health_width, 5))
            
            # Draw mana bar
            mana_width = (self.width * self.mana) // self.max_mana
            pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y - 5, self.width, 3))
            pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y - 5, mana_width, 3))
            
        except Exception as e:
            raise StateError(f"Failed to draw player: {str(e)}")
            
    def to_dict(self):
        """Convert player state to dictionary"""
        try:
            return {
                'x': self.x,
                'y': self.y,
                'health': self.health,
                'max_health': self.max_health,
                'mana': self.mana,
                'max_mana': self.max_mana,
                'level': self.level,
                'xp': self.xp,
                'xp_to_next_level': self.xp_to_next_level,
                'inventory': self.inventory,
                'selected_item': self.selected_item,
                'spell_levels': self.spell_levels,
                'current_spell': self.current_spell,
                'speed': self.speed
            }
        except Exception as e:
            raise StateError(f"Failed to serialize player: {str(e)}")
            
    def from_dict(self, data):
        """Load player state from dictionary"""
        try:
            self.x = data['x']
            self.y = data['y']
            self.health = data['health']
            self.max_health = data['max_health']
            self.mana = data['mana']
            self.max_mana = data['max_mana']
            self.level = data['level']
            self.xp = data['xp']
            self.xp_to_next_level = data['xp_to_next_level']
            self.inventory = data['inventory']
            self.selected_item = data['selected_item']
            self.spell_levels = data['spell_levels']
            self.current_spell = data['current_spell']
            self.speed = data['speed']
            
        except Exception as e:
            raise StateError(f"Failed to deserialize player: {str(e)}")