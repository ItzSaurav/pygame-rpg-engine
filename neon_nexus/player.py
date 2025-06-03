# player.py
import pygame
from collections import defaultdict
import math
import random
from projectile import Projectile

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
        # Draw player body
        pygame.draw.rect(self.surface, (100, 200, 255), (0, 0, self.width, self.height))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.width, self.height), 2)
        
        # Draw eyes
        eye_color = (255, 255, 255) if not self.jumping else (255, 100, 100)
        pygame.draw.circle(self.surface, eye_color, (self.width//4, self.height//3), 4)
        pygame.draw.circle(self.surface, eye_color, (3*self.width//4, self.height//3), 4)
        
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
    
    def update(self):
        # Update jump physics
        self.update_jump()
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.spell_cooldown > 0:
            self.spell_cooldown -= 1
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= 1
        
        # Update attack charge
        if self.attack_charge < self.max_attack_charge:
            self.attack_charge += 1
        
        # Regenerate mana
        if self.mana < self.max_mana:
            self.mana = min(self.max_mana, self.mana + self.mana_regen)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.active:
                self.projectiles.remove(projectile)
        
        # Update level-up effect
        self.update_level_up_effect()
    
    def draw(self, screen, camera):
        # Calculate screen position
        screen_x, screen_y = camera.apply(self)
        
        # Draw player
        screen.blit(self.surface, (screen_x, screen_y))
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
        
        # Draw level-up effect
        self.draw_level_up_effect(screen, camera)
        
        # Draw health bar
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
        
        # Draw mana bar
        mana_width = 40
        mana_height = 4
        mana_x = screen_x + (self.width - mana_width) // 2
        mana_y = screen_y - 5
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), 
                        (mana_x, mana_y, mana_width, mana_height))
        # Mana
        mana_color = {
            "fire": (255, 100, 0),
            "ice": (100, 200, 255),
            "lightning": (255, 255, 100)
        }[self.current_spell]
        pygame.draw.rect(screen, mana_color, 
                        (mana_x, mana_y, 
                         int(mana_width * self.mana / self.max_mana), mana_height))
        
        # Draw attack charge bar
        if self.attack_charge > 0:
            charge_width = 40
            charge_height = 2
            charge_x = screen_x + (self.width - charge_width) // 2
            charge_y = screen_y - 15
            
            # Background
            pygame.draw.rect(screen, (100, 100, 100), 
                           (charge_x, charge_y, charge_width, charge_height))
            # Charge
            charge_percent = self.attack_charge / self.max_attack_charge
            charge_color = (255, 200, 50) if charge_percent >= 1 else (200, 200, 50)
            pygame.draw.rect(screen, charge_color, 
                           (charge_x, charge_y, 
                            int(charge_width * charge_percent), charge_height))
    
    def to_dict(self):
        """Convert player data to dictionary for saving"""
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
    
    @classmethod
    def from_dict(cls, data):
        """Create player from saved data"""
        player = cls(data['x'], data['y'])
        player.health = data['health']
        player.max_health = data['max_health']
        player.mana = data['mana']
        player.max_mana = data['max_mana']
        player.level = data['level']
        player.xp = data['xp']
        player.xp_to_next_level = data['xp_to_next_level']
        player.inventory = data['inventory']
        player.selected_item = data['selected_item']
        player.spell_levels = data['spell_levels']
        player.current_spell = data['current_spell']
        player.speed = data['speed']
        return player