import logging
import traceback
import pygame
import sys
from datetime import datetime
import os

class GameError(Exception):
    """Base exception class for game-specific errors"""
    pass

class ResourceError(GameError):
    """Raised when there are issues loading game resources"""
    pass

class SaveError(GameError):
    """Raised when there are issues with save/load operations"""
    pass

class StateError(GameError):
    """Raised when there are issues with game state transitions"""
    pass

class InputError(GameError):
    """Raised when there are issues with input handling"""
    pass

class WorldError(GameError):
    """Raised when there are issues with world generation or updates"""
    pass

class ErrorHandler:
    def __init__(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Set up logging
        log_file = f'logs/neon_nexus_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Initialize error counts
        self.error_counts = {
            'ResourceError': 0,
            'SaveError': 0,
            'StateError': 0,
            'InputError': 0,
            'WorldError': 0,
            'Other': 0
        }
        
        # Maximum errors before forced shutdown
        self.max_errors = 10
        
    def handle_error(self, error, error_type=None, context=None):
        """Handle different types of errors with appropriate responses"""
        error_type = error_type or type(error).__name__
        
        # Log the error
        logging.error(f"Error Type: {error_type}")
        logging.error(f"Error Message: {str(error)}")
        if context:
            logging.error(f"Context: {context}")
        logging.error(f"Traceback:\n{traceback.format_exc()}")
        
        # Update error count
        if error_type in self.error_counts:
            self.error_counts[error_type] += 1
        else:
            self.error_counts['Other'] += 1
            
        # Check if we've exceeded max errors
        total_errors = sum(self.error_counts.values())
        if total_errors >= self.max_errors:
            self.handle_critical_error("Maximum error threshold exceeded")
            
        # Handle specific error types
        if isinstance(error, ResourceError):
            self.handle_resource_error(error)
        elif isinstance(error, SaveError):
            self.handle_save_error(error)
        elif isinstance(error, StateError):
            self.handle_state_error(error)
        elif isinstance(error, InputError):
            self.handle_input_error(error)
        elif isinstance(error, WorldError):
            self.handle_world_error(error)
        else:
            self.handle_unknown_error(error)
            
    def handle_resource_error(self, error):
        """Handle resource loading errors"""
        logging.warning("Attempting to recover from resource error...")
        # Add resource recovery logic here
        
    def handle_save_error(self, error):
        """Handle save/load errors"""
        logging.warning("Attempting to recover from save error...")
        # Add save recovery logic here
        
    def handle_state_error(self, error):
        """Handle game state errors"""
        logging.warning("Attempting to recover from state error...")
        # Add state recovery logic here
        
    def handle_input_error(self, error):
        """Handle input handling errors"""
        logging.warning("Attempting to recover from input error...")
        # Add input recovery logic here
        
    def handle_world_error(self, error):
        """Handle world generation/update errors"""
        logging.warning("Attempting to recover from world error...")
        # Add world recovery logic here
        
    def handle_unknown_error(self, error):
        """Handle unknown errors"""
        logging.warning("Attempting to recover from unknown error...")
        # Add general recovery logic here
        
    def handle_critical_error(self, message):
        """Handle critical errors that require game shutdown"""
        logging.critical(f"Critical Error: {message}")
        logging.critical("Forcing game shutdown...")
        pygame.quit()
        sys.exit(1)
        
    def get_error_summary(self):
        """Get a summary of all errors encountered"""
        return {
            'total_errors': sum(self.error_counts.values()),
            'error_breakdown': self.error_counts.copy()
        } 