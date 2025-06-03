import pygame

class Portal:
    def __init__(self, chunk_x, chunk_y, x, y, unlocked=False, name=None):
        self.chunk_x = chunk_x  # Chunk coordinates
        self.chunk_y = chunk_y
        self.x = x  # Position within chunk
        self.y = y
        self.unlocked = unlocked
        self.name = name or f"Portal ({chunk_x},{chunk_y})"
        self.radius = 12
        self.color_locked = (100, 100, 200)
        self.color_unlocked = (255, 255, 100)
        self.glow_color = (100, 200, 255, 100)

    def draw(self, screen, camera, chunk_size):
        # Calculate world position
        world_x = self.chunk_x * chunk_size + self.x
        world_y = self.chunk_y * chunk_size + self.y
        screen_x, screen_y = camera.apply_obj(world_x, world_y)
        # Draw glow
        glow = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
        pygame.draw.circle(glow, self.glow_color, (self.radius*2, self.radius*2), self.radius*2)
        screen.blit(glow, (screen_x - self.radius, screen_y - self.radius), special_flags=pygame.BLEND_RGBA_ADD)
        # Draw portal
        color = self.color_unlocked if self.unlocked else self.color_locked
        pygame.draw.circle(screen, color, (screen_x, screen_y), self.radius)
        pygame.draw.circle(screen, (255,255,255), (screen_x, screen_y), self.radius, 2)
        # Draw name if unlocked
        if self.unlocked:
            font = pygame.font.Font(None, 18)
            text = font.render(self.name, True, (255,255,200))
            screen.blit(text, (screen_x - text.get_width()//2, screen_y - self.radius - 18))

    def to_dict(self):
        return {
            'chunk_x': self.chunk_x,
            'chunk_y': self.chunk_y,
            'x': self.x,
            'y': self.y,
            'unlocked': self.unlocked,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['chunk_x'],
            data['chunk_y'],
            data['x'],
            data['y'],
            unlocked=data.get('unlocked', False),
            name=data.get('name')
        ) 