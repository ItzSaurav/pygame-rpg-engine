import pygame
import math

class Joystick:
    def __init__(self, x, y, base_radius=50, thumb_radius=20):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.thumb_radius = thumb_radius
        self.thumb_x = x
        self.thumb_y = y
        self.dragging = False
        self.vector = (0, 0)
        self.max_distance = base_radius - thumb_radius
        self.return_speed = 0.2
        self.active = False
        
        # Colors
        self.base_color = (50, 50, 150, 128)  # Semi-transparent blue
        self.thumb_color = (100, 200, 255)    # Bright neon blue
        self.glow_color = (100, 200, 255, 64) # Glow effect
        self.active_color = (150, 250, 255)   # Brighter when active
        
        # Create surfaces
        self.base_surface = pygame.Surface((base_radius * 2, base_radius * 2), pygame.SRCALPHA)
        self.thumb_surface = pygame.Surface((thumb_radius * 2, thumb_radius * 2), pygame.SRCALPHA)
        self.glow_surface = pygame.Surface((base_radius * 2, base_radius * 2), pygame.SRCALPHA)
        
        # Draw base
        pygame.draw.circle(self.base_surface, self.base_color, (base_radius, base_radius), base_radius)
        pygame.draw.circle(self.base_surface, (255, 255, 255, 64), (base_radius, base_radius), base_radius, 2)
        
        # Draw thumb
        pygame.draw.circle(self.thumb_surface, self.thumb_color, (thumb_radius, thumb_radius), thumb_radius)
        pygame.draw.circle(self.thumb_surface, (255, 255, 255, 128), (thumb_radius, thumb_radius), thumb_radius, 2)
        
        # Draw glow
        pygame.draw.circle(self.glow_surface, self.glow_color, (base_radius, base_radius), base_radius)
        
        # Create arrow indicators
        self.arrow_surface = pygame.Surface((base_radius * 2, base_radius * 2), pygame.SRCALPHA)
        self._draw_arrows()
    
    def _draw_arrows(self):
        """Draw directional arrows on the joystick base"""
        center = (self.base_radius, self.base_radius)
        arrow_length = self.base_radius * 0.6
        arrow_width = 4
        
        # Draw arrows in 8 directions
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            end_x = center[0] + math.cos(rad) * arrow_length
            end_y = center[1] + math.sin(rad) * arrow_length
            
            # Draw arrow line
            pygame.draw.line(self.arrow_surface, (255, 255, 255, 32),
                           center, (end_x, end_y), arrow_width)
            
            # Draw arrow head
            head_angle1 = rad + math.radians(150)
            head_angle2 = rad - math.radians(150)
            head_length = 8
            
            head1_x = end_x + math.cos(head_angle1) * head_length
            head1_y = end_y + math.sin(head_angle1) * head_length
            head2_x = end_x + math.cos(head_angle2) * head_length
            head2_y = end_y + math.sin(head_angle2) * head_length
            
            pygame.draw.line(self.arrow_surface, (255, 255, 255, 32),
                           (end_x, end_y), (head1_x, head1_y), arrow_width)
            pygame.draw.line(self.arrow_surface, (255, 255, 255, 32),
                           (end_x, end_y), (head2_x, head2_y), arrow_width)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if click is within base radius
                dx = event.pos[0] - self.x
                dy = event.pos[1] - self.y
                if math.sqrt(dx*dx + dy*dy) <= self.base_radius:
                    self.dragging = True
                    self.active = True
                    self._update_thumb_position(event.pos)
                    return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                self.active = False
                self.vector = (0, 0)
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_thumb_position(event.pos)
                return True
        return False
    
    def _update_thumb_position(self, pos):
        """Update thumb position based on mouse/touch position"""
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize and clamp distance
            if distance > self.max_distance:
                dx = dx * self.max_distance / distance
                dy = dy * self.max_distance / distance
                distance = self.max_distance
            
            # Update thumb position
            self.thumb_x = self.x + dx
            self.thumb_y = self.y + dy
            
            # Calculate movement vector
            self.vector = (dx / self.max_distance, dy / self.max_distance)
        else:
            self.vector = (0, 0)
    
    def update(self):
        """Update joystick state"""
        if not self.dragging:
            # Return thumb to center
            dx = self.x - self.thumb_x
            dy = self.y - self.thumb_y
            self.thumb_x += dx * self.return_speed
            self.thumb_y += dy * self.return_speed
            
            # Update vector
            distance = math.sqrt(dx*dx + dy*dy)
            if distance < 1:
                self.thumb_x = self.x
                self.thumb_y = self.y
                self.vector = (0, 0)
    
    def draw(self, screen):
        """Draw the joystick"""
        # Draw base
        screen.blit(self.base_surface, (self.x - self.base_radius, self.y - self.base_radius))
        
        # Draw glow when active
        if self.active:
            screen.blit(self.glow_surface, (self.x - self.base_radius, self.y - self.base_radius))
        
        # Draw arrows
        screen.blit(self.arrow_surface, (self.x - self.base_radius, self.y - self.base_radius))
        
        # Draw thumb
        thumb_color = self.active_color if self.active else self.thumb_color
        pygame.draw.circle(screen, thumb_color, (int(self.thumb_x), int(self.thumb_y)), self.thumb_radius)
        pygame.draw.circle(screen, (255, 255, 255, 128), (int(self.thumb_x), int(self.thumb_y)), self.thumb_radius, 2)
        
        # Draw direction indicator when active
        if self.active and self.vector != (0, 0):
            end_x = self.x + self.vector[0] * self.base_radius
            end_y = self.y + self.vector[1] * self.base_radius
            pygame.draw.line(screen, (255, 255, 255, 128), 
                           (self.x, self.y), (end_x, end_y), 2) 