import json
import os
from areas import Area, AreaType, GateType

class SaveManager:
    def __init__(self):
        self.save_dir = 'neon_nexus/saves'
        self.save_file = os.path.join(self.save_dir, 'save.json')
        self.ensure_save_dir()
    
    def ensure_save_dir(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_exists(self):
        """Check if a save file exists"""
        return os.path.exists(self.save_file)
    
    def save_game(self, game):
        """Save the current game state"""
        save_data = {
            'player': game.player.to_dict(),
            'world': game.world.to_dict(),
            'camera': {
                'x': game.camera.x,
                'y': game.camera.y,
                'target': {
                    'x': game.camera.target.x,
                    'y': game.camera.target.y
                }
            }
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, game):
        """Load a saved game state"""
        if not self.save_exists():
            return False
        
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            # Load player data
            game.player = game.player.from_dict(save_data['player'])
            
            # Load world data
            game.world = game.world.from_dict(save_data['world'])
            
            # Load camera data
            game.camera.x = save_data['camera']['x']
            game.camera.y = save_data['camera']['y']
            game.camera.target.x = save_data['camera']['target']['x']
            game.camera.target.y = save_data['camera']['target']['y']
            
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False 