import pygame

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.color = (180, 120, 60)
        self.is_pushed = False
        self.velocity = [0, 0]
    def update(self):
        # TODO: Add physics and collision
        pass
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self)
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'is_pushed': self.is_pushed,
            'velocity': self.velocity
        }
    @classmethod
    def from_dict(cls, data):
        box = cls(data['x'], data['y'])
        box.is_pushed = data.get('is_pushed', False)
        box.velocity = data.get('velocity', [0, 0])
        return box

class Lever:
    def __init__(self, x, y, linked_object=None):
        self.x = x
        self.y = y
        self.state = False
        self.linked_object = linked_object
    def interact(self):
        self.state = not self.state
        if self.linked_object:
            self.linked_object.toggle()
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply_obj(self.x, self.y)
        color = (100, 255, 100) if self.state else (100, 100, 100)
        pygame.draw.rect(screen, color, (screen_x, screen_y, 12, 24))
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'state': self.state
        }
    @classmethod
    def from_dict(cls, data):
        lever = cls(data['x'], data['y'])
        lever.state = data.get('state', False)
        return lever

class PressurePlate:
    def __init__(self, x, y, linked_object=None):
        self.x = x
        self.y = y
        self.activated = False
        self.linked_object = linked_object
    def update(self, player):
        # TODO: Check if player or box is on plate
        pass
    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply_obj(self.x, self.y)
        color = (200, 200, 100) if self.activated else (120, 120, 60)
        pygame.draw.rect(screen, color, (screen_x, screen_y, 20, 6))
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'activated': self.activated
        }
    @classmethod
    def from_dict(cls, data):
        plate = cls(data['x'], data['y'])
        plate.activated = data.get('activated', False)
        return plate

class DestructibleBlock:
    def __init__(self, x, y, hp=1):
        self.x = x
        self.y = y
        self.hp = hp
        self.destroyed = False
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.destroyed = True
    def draw(self, screen, camera):
        if not self.destroyed:
            screen_x, screen_y = camera.apply_obj(self.x, self.y)
            pygame.draw.rect(screen, (180, 60, 60), (screen_x, screen_y, 24, 24))
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'hp': self.hp,
            'destroyed': self.destroyed
        }
    @classmethod
    def from_dict(cls, data):
        block = cls(data['x'], data['y'], data.get('hp', 1))
        block.destroyed = data.get('destroyed', False)
        return block 