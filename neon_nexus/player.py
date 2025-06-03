# player.py
import pygame

class Player:
    def __init__(self, x=0, y=0):
        self.level = 1
        self.xp = 0
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load('neon_nexus/assets/player.png').convert_alpha()
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 100:
            self.level_up()
            
    def level_up(self):
        self.level += 1
        self.speed += 0.2
        print(f"Level up! Now level {self.level}")
    
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self)
        scaled_size = int(32 * camera.zoom)  # 32 is the original image size
        scaled_image = pygame.transform.scale(self.image, (scaled_size, scaled_size))
        screen.blit(scaled_image, (screen_x - scaled_size//2, screen_y - scaled_size//2))