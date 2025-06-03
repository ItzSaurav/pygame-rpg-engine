import pygame
import sys
import time
from player import Player
from world import World
from camera import Camera
from save_manager import SaveManager
from joystick import Joystick
from error_handler import ErrorHandler, GameError, ResourceError, SaveError, StateError, InputError, WorldError

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

MENU_BG = (20, 20, 40)
MENU_TEXT = (255, 255, 255)
MENU_SELECTED = (100, 200, 255)
MENU_DISABLED = (100, 100, 100)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, draggable=False, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        self.draggable = draggable
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.cooldown = 0
        self.cooldown_time = 0
        self.charge = 0
        self.max_charge = 0
        self.icon = icon
        self.disabled = False
        self.alpha = 255
        self.target_alpha = 255
        self.fade_speed = 5
    
    def draw(self, screen):
        # Fade animation
        if self.alpha != self.target_alpha:
            self.alpha = max(0, min(255, self.alpha + (self.target_alpha - self.alpha) * 0.1))
        
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        if self.cooldown > 0:
            color = tuple(max(0, c - 100) for c in color)
        if self.disabled:
            color = MENU_DISABLED
        
        # Create surface with alpha
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*color, self.alpha), button_surface.get_rect(), border_radius=10)
        pygame.draw.rect(button_surface, (255, 255, 255, self.alpha), button_surface.get_rect(), 2, border_radius=10)
        
        # Draw icon if present
        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.rect.width//4, self.rect.height//2))
            button_surface.blit(self.icon, icon_rect)
        
        # Draw text
        text_color = (255, 255, 255, self.alpha) if not self.disabled else (150, 150, 150, self.alpha)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.rect.width//2 + (self.icon.get_width()//2 if self.icon else 0), 
                                                 self.rect.height//2))
        button_surface.blit(text_surface, text_rect)
        
        # Draw cooldown overlay
        if self.cooldown > 0:
            cooldown_height = self.rect.height * (self.cooldown / self.cooldown_time)
            cooldown_rect = pygame.Rect(
                0,
                self.rect.height - cooldown_height,
                self.rect.width,
                cooldown_height
            )
            pygame.draw.rect(button_surface, (0, 0, 0, 128), cooldown_rect)
        
        # Draw charge indicator
        if self.max_charge > 0:
            charge_width = self.rect.width * (self.charge / self.max_charge)
            charge_rect = pygame.Rect(
                0,
                -5,
                charge_width,
                3
            )
            charge_color = (255, 200, 50, self.alpha) if self.charge >= self.max_charge else (200, 200, 50, self.alpha)
            pygame.draw.rect(button_surface, charge_color, charge_rect)
        
        # Blit the button surface onto the screen
        screen.blit(button_surface, self.rect)
    
    def handle_event(self, event):
        if self.disabled:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            if self.dragging and self.draggable:
                self.rect.x = event.pos[0] - self.drag_offset_x
                self.rect.y = event.pos[1] - self.drag_offset_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.cooldown <= 0:
                if self.draggable:
                    self.dragging = True
                    self.drag_offset_x = event.pos[0] - self.rect.x
                    self.drag_offset_y = event.pos[1] - self.rect.y
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        return False
    
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

class Game:
    def __init__(self):
        try:
            # Initialize error handler
            self.error_handler = ErrorHandler()
            
            # Initialize pygame
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Neon Nexus")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            
            # Initialize game components
            self._initialize_components()
            
        except pygame.error as e:
            self.error_handler.handle_error(e, "ResourceError", "Failed to initialize pygame")
            raise
        except Exception as e:
            self.error_handler.handle_error(e, "ResourceError", "Failed to initialize game")
            raise
            
    def _initialize_components(self):
        """Initialize game components with error handling"""
        try:
            # Save system
            self.save_manager = SaveManager()
            
            # Game objects
            self.world = World()
            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.camera = Camera(self.player)
            self.player.camera = self.camera
            
            # Game state
            self.running = True
            self.fps = FPS
            self.show_inventory = False
            self.last_time = time.time()
            self.frame_times = []
            self.state = 'menu'
            self.menu_options = ["New Game", "Continue", "Settings", "Controls", "Quit"]
            self.menu_selected = 0
            self.settings_options = ["(No settings yet)", "Back"]
            self.settings_selected = 0
            
            # Create menu buttons
            self._create_menu_buttons()
            
            # Create joystick
            self.joystick = Joystick(
                self.button_margin + 50,
                SCREEN_HEIGHT - self.button_margin - 50,
                base_radius=50,
                thumb_radius=20
            )
            
        except Exception as e:
            self.error_handler.handle_error(e, "ResourceError", "Failed to initialize game components")
            raise
            
    def _create_menu_buttons(self):
        """Create menu buttons with error handling"""
        try:
            self.button_width = 100
            self.button_height = 50
            self.button_margin = 20
            start_y = 200
            
            self.menu_buttons = []
            for i, option in enumerate(self.menu_options):
                button = Button(
                    SCREEN_WIDTH//2 - self.button_width//2,
                    start_y + i * (self.button_height + self.button_margin),
                    self.button_width,
                    self.button_height,
                    option,
                    (50, 50, 150),
                    (70, 70, 170)
                )
                self.menu_buttons.append(button)
                
        except Exception as e:
            self.error_handler.handle_error(e, "ResourceError", "Failed to create menu buttons")
            raise
            
    def run(self):
        """Main game loop with error handling"""
        try:
            while self.running:
                try:
                    self._handle_events()
                    self._update()
                    self._draw()
                    self.clock.tick(self.fps)
                    
                except InputError as e:
                    self.error_handler.handle_error(e, "InputError", "Error handling input")
                except StateError as e:
                    self.error_handler.handle_error(e, "StateError", "Error updating game state")
                except WorldError as e:
                    self.error_handler.handle_error(e, "WorldError", "Error updating world")
                except Exception as e:
                    self.error_handler.handle_error(e, "Unknown", "Unexpected error in game loop")
                    
        except Exception as e:
            self.error_handler.handle_error(e, "Critical", "Critical error in main game loop")
            raise
        finally:
            self._cleanup()
            
    def _handle_events(self):
        """Handle game events with error handling"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mousedown(event)
                    
        except Exception as e:
            raise InputError(f"Error handling events: {str(e)}")
            
    def _update(self):
        """Update game state with error handling"""
        try:
            if self.state == 'game':
                self.world.update(self.camera, self.player)
                self.player.update()
                self.camera.update()
                
        except Exception as e:
            raise StateError(f"Error updating game state: {str(e)}")
            
    def _draw(self):
        """Draw game state with error handling"""
        try:
            self.screen.fill((0, 0, 0))
            
            if self.state == 'game':
                self.world.draw(self.screen, self.camera)
                self.player.draw(self.screen, self.camera)
                self.joystick.draw(self.screen)
            elif self.state == 'menu':
                self._draw_menu()
            elif self.state == 'settings':
                self._draw_settings()
            elif self.state == 'controls':
                self._draw_controls()
                
            pygame.display.flip()
            
        except Exception as e:
            raise StateError(f"Error drawing game state: {str(e)}")
            
    def _cleanup(self):
        """Clean up resources with error handling"""
        try:
            # Save game state if needed
            if self.state == 'game':
                self.save_manager.save_game(self)
                
            # Quit pygame
            pygame.quit()
            
        except Exception as e:
            self.error_handler.handle_error(e, "Cleanup", "Error during cleanup")
            
    def _draw_menu(self):
        self.screen.fill(MENU_BG)
        
        # Draw title with glow effect
        title = self.font.render("Neon Nexus", True, MENU_TEXT)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        
        # Draw glow
        for i in range(3):
            glow = self.font.render("Neon Nexus", True, (100, 200, 255, 100))
            glow_rect = glow.get_rect(center=(SCREEN_WIDTH//2 + i*2, 80 + i*2))
            self.screen.blit(glow, glow_rect)
        
        self.screen.blit(title, title_rect)
        
        # Draw menu buttons
        for button in self.menu_buttons:
            button.draw(self.screen)
        
        pygame.display.flip()
    
    def _draw_settings(self):
        self.screen.fill(MENU_BG)
        title = self.font.render("Settings", True, MENU_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        for i, option in enumerate(self.settings_options):
            color = MENU_SELECTED if i == self.settings_selected else MENU_TEXT
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*60))
        pygame.display.flip()
    
    def _draw_controls(self):
        self.screen.fill(MENU_BG)
        title = self.font.render("Controls", True, MENU_TEXT)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        controls = [
            "WASD: Move",
            "SPACE: Jump",
            "I: Toggle Inventory",
            "M: Toggle Map",
            "1: Select First Item",
            "ESC: Menu/Pause",
            "ENTER: Select Menu Option",
            "UP/DOWN: Navigate Menu",
            "Click Jump/Attack buttons or use SPACE"
        ]
        for i, line in enumerate(controls):
            text = self.small_font.render(line, True, MENU_TEXT)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 180 + i*40))
        info = self.small_font.render("Press ESC or ENTER to return", True, (180, 180, 255))
        self.screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, 450))
        pygame.display.flip()
    
    def _draw_hud(self):
        # FPS counter
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        fps = 1 / avg_frame_time if avg_frame_time > 0 else 0
        fps_text = self.small_font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))
        
        # Level and XP
        level_text = self.small_font.render(f"Level: {self.player.level}", True, (255, 255, 255))
        xp_text = self.small_font.render(f"XP: {self.player.xp}/{self.player.level * 100}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(xp_text, (10, 70))
        
        # Inventory
        if self.show_inventory:
            inventory_surface = pygame.Surface((200, 300))
            inventory_surface.fill((50, 50, 50))
            inventory_surface.set_alpha(200)
            
            y = 10
            for item, quantity in self.player.inventory.items():
                item_text = self.small_font.render(f"{item}: {quantity}", True, (255, 255, 255))
                inventory_surface.blit(item_text, (10, y))
                y += 30
            
            self.screen.blit(inventory_surface, (600, 10))
        
        # Draw controls
        self.joystick.draw(self.screen)
        self.jump_button.draw(self.screen)
        self.attack_button.draw(self.screen)
        self.spell_button.draw(self.screen)
        
        # Draw spell selection buttons
        for button in self.spell_buttons:
            button.draw(self.screen)
        
        # Draw spell level indicators
        spell_types = ["fire", "ice", "lightning"]
        for i, spell_type in enumerate(spell_types):
            level = self.player.spell_levels[spell_type]
            level_text = self.small_font.render(f"Lvl {level}", True, (255, 255, 255))
            level_x = SCREEN_WIDTH - self.button_width * 4 - self.button_margin * 4
            level_y = SCREEN_HEIGHT - self.button_height * 2 - self.button_margin * 2 + i * (self.button_height + 10) - 20
            self.screen.blit(level_text, (level_x, level_y))
        
        # Draw debug info if enabled
        if self.show_debug:
            debug_y = 100
            debug_info = [
                f"Player Y: {self.player.y:.1f}",
                f"Velocity Y: {self.player.velocity_y:.1f}",
                f"On Ground: {self.player.on_ground}",
                f"Jumping: {self.player.jumping}",
                f"Camera Y: {self.camera.y:.1f}",
                f"Target Y: {self.camera.target.y:.1f}",
                f"Joystick Vector: {self.joystick.vector}",
                f"Mana: {self.player.mana:.1f}/{self.player.max_mana}",
                f"Current Spell: {self.player.current_spell}",
                f"Spell Cooldown: {self.player.spell_cooldown}"
            ]
            
            for line in debug_info:
                text = self.debug_font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, debug_y))
                debug_y += 20
    
    def _handle_keydown(self, event):
        if self.state == 'menu':
            if event.key == pygame.K_UP:
                self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._handle_menu_select()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == 'settings':
            if event.key == pygame.K_UP:
                self.settings_selected = (self.settings_selected - 1) % len(self.settings_options)
            elif event.key == pygame.K_DOWN:
                self.settings_selected = (self.settings_selected + 1) % len(self.settings_options)
            elif event.key == pygame.K_RETURN:
                if self.settings_options[self.settings_selected] == "Back":
                    self.state = 'menu'
            elif event.key == pygame.K_ESCAPE:
                self.state = 'menu'
        elif self.state == 'controls':
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.state = 'menu'
        elif self.state == 'playing':
            if event.key == pygame.K_ESCAPE:
                self.save_manager.save_game(self)
                self.state = 'menu'
            elif event.key == pygame.K_i:
                self.show_inventory = not self.show_inventory
            elif event.key == pygame.K_m:  # Toggle map
                self.world.world_map.toggle()
            elif event.key == pygame.K_t:  # Fast travel UI
                self.show_fast_travel = not self.show_fast_travel
            elif event.key == pygame.K_e:  # Environmental interaction
                self._interact_with_environment()
            elif event.key == pygame.K_1:
                self.player.selected_item = list(self.player.inventory.keys())[0] if self.player.inventory else None
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        
        if event.key == pygame.K_F3:  # Toggle debug info
            self.show_debug = not self.show_debug
    
    def _handle_menu_select(self):
        option = self.menu_options[self.menu_selected]
        if option == "New Game":
            self.__init__()
            self.state = 'playing'
        elif option == "Continue":
            if self.save_manager.load_game(self):
                self.state = 'playing'
        elif option == "Settings":
            self.state = 'settings'
        elif option == "Controls":
            self.state = 'controls'
        elif option == "Quit":
            self.running = False
    
    def _interact_with_environment(self):
        # Check for nearby levers, boxes, etc., and interact
        player_chunk_x = int(self.player.x // self.world.chunk_size)
        player_chunk_y = int(self.player.y // self.world.chunk_size)
        for lever in self.world.levers:
            if lever.chunk_x == player_chunk_x and lever.chunk_y == player_chunk_y:
                dx = self.player.x - (lever.chunk_x * self.world.chunk_size + lever.x)
                dy = self.player.y - (lever.chunk_y * self.world.chunk_size + lever.y)
                distance = (dx * dx + dy * dy) ** 0.5
                if distance < 50:  # Interact if within 50 pixels
                    lever.interact()
        for box in self.world.boxes:
            if box.chunk_x == player_chunk_x and box.chunk_y == player_chunk_y:
                dx = self.player.x - (box.chunk_x * self.world.chunk_size + box.x)
                dy = self.player.y - (box.chunk_y * self.world.chunk_size + box.y)
                distance = (dx * dx + dy * dy) ** 0.5
                if distance < 50:  # Push if within 50 pixels
                    box.is_pushed = True
                    # TODO: Add physics for pushing

def main():
    """Main entry point with error handling"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Critical error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit(1)
        
if __name__ == "__main__":
    main()