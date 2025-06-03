import json
import os
from error_handler import SaveError

class SaveManager:
    def __init__(self):
        self.save_dir = "saves"
        self.save_file = "save.json"
        self._ensure_save_dir()
        
    def _ensure_save_dir(self):
        """Ensure save directory exists"""
        try:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
        except Exception as e:
            raise SaveError(f"Failed to create save directory: {str(e)}")
            
    def save_exists(self):
        """Check if a save file exists"""
        try:
            return os.path.exists(os.path.join(self.save_dir, self.save_file))
        except Exception as e:
            raise SaveError(f"Failed to check save existence: {str(e)}")
            
    def save_game(self, game):
        """Save game state"""
        try:
            save_data = {
                'player': game.player.to_dict(),
                'world': game.world.to_dict(),
                'camera': {
                    'x': game.camera.x,
                    'y': game.camera.y
                }
            }
            
            with open(os.path.join(self.save_dir, self.save_file), 'w') as f:
                json.dump(save_data, f, indent=4)
                
        except Exception as e:
            raise SaveError(f"Failed to save game: {str(e)}")
            
    def load_game(self, game):
        """Load game state"""
        try:
            if not self.save_exists():
                return False
                
            with open(os.path.join(self.save_dir, self.save_file), 'r') as f:
                save_data = json.load(f)
                
            # Load player data
            game.player = game.player.from_dict(save_data['player'])
            
            # Load world data
            game.world = game.world.from_dict(save_data['world'])
            
            # Load camera data
            game.camera.x = save_data['camera']['x']
            game.camera.y = save_data['camera']['y']
            
            return True
            
        except json.JSONDecodeError as e:
            raise SaveError(f"Failed to parse save file: {str(e)}")
        except Exception as e:
            raise SaveError(f"Failed to load game: {str(e)}")
            
    def create_backup(self):
        """Create a backup of the current save file"""
        try:
            if not self.save_exists():
                return
                
            backup_file = f"save_backup_{int(time.time())}.json"
            with open(os.path.join(self.save_dir, self.save_file), 'r') as src:
                with open(os.path.join(self.save_dir, backup_file), 'w') as dst:
                    dst.write(src.read())
                    
        except Exception as e:
            raise SaveError(f"Failed to create save backup: {str(e)}")
            
    def restore_backup(self, backup_file):
        """Restore from a backup save file"""
        try:
            if not os.path.exists(os.path.join(self.save_dir, backup_file)):
                raise SaveError(f"Backup file {backup_file} not found")
                
            with open(os.path.join(self.save_dir, backup_file), 'r') as src:
                with open(os.path.join(self.save_dir, self.save_file), 'w') as dst:
                    dst.write(src.read())
                    
        except Exception as e:
            raise SaveError(f"Failed to restore backup: {str(e)}") 