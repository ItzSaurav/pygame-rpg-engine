import pygame
import random

class Enemy:
    def __init__(self, x, y, enemy_type="slime"):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.hp = 20
        self.max_hp = 20
        self.aggro_radius = 100
        self.patrol_range = 60
        self.state = "patrol"
        self.direction = 1
        self.speed = 1.0
        self.attack_cooldown = 0
    def update(self, player):
        # TODO: Add patrol and aggro logic
        pass
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self)
        color = (100, 200, 100) if self.type == "slime" else (200, 100, 100)
        pygame.draw.circle(screen, color, (screen_x, screen_y), 16)
        # Draw HP bar
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (255,0,0), (screen_x-16, screen_y-24, 32, 4))
        pygame.draw.rect(screen, (0,255,0), (screen_x-16, screen_y-24, int(32*hp_ratio), 4))

class Boss(Enemy):
    def __init__(self, x, y, boss_type="golem"):
        super().__init__(x, y, enemy_type=boss_type)
        self.phase = 1
        self.max_hp = 200
        self.hp = 200
        self.attack_patterns = ["slam", "projectile"]
        self.current_pattern = 0
    def update(self, player):
        # TODO: Add multi-phase and attack pattern logic
        pass
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self)
        pygame.draw.circle(screen, (180, 80, 80), (screen_x, screen_y), 32)
        # Boss HP bar
        pygame.draw.rect(screen, (0,0,0), (screen_x-40, screen_y-48, 80, 8))
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (255,0,0), (screen_x-40, screen_y-48, 80, 8))
        pygame.draw.rect(screen, (0,255,0), (screen_x-40, screen_y-48, int(80*hp_ratio), 8)) 