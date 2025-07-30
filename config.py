"""Configuration management for the banking application."""

import json
import os
from typing import Dict, Any, Optional
from logging_config import banking_logger

logger = banking_logger.get_logger("Config")

class Config:
    """Configuration manager for the banking application."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_default_config()
        self.load_config()
    
    def load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "database": {
                "path": "banque.db",
                "backup_enabled": True,
                "backup_interval": 24,  # hours
                "max_backups": 7
            },
            "ui": {
                "language": "en",
                "theme": "default",
                "window_size": "1600x800",
                "auto_save": True
            },
            "logging": {
                "level": "INFO",
                "file_enabled": True,
                "console_enabled": True,
                "max_file_size": 10,  # MB
                "backup_count": 5
            },
            "security": {
                "encrypt_sensitive_data": False,
                "session_timeout": 30,  # minutes
                "max_login_attempts": 3
            },
            "performance": {
                "cache_enabled": True,
                "cache_size": 100,
                "async_operations": True,
                "batch_size": 50
            }
        }
    
    def load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    # Merge with default config
                    self.merge_config(self.config, file_config)
                logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.save_config()
                logger.info("Default configuration created")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
    
    def merge_config(self, default: Dict, override: Dict):
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                self.merge_config(default[key], value)
            else:
                default[key] = value
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        keys = key.split(".")
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (supports dot notation)."""
        keys = key.split(".")
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")
    
    def get_database_path(self) -> str:
        """Get database file path."""
        return self.get("database.path", "banque.db")
    
    def get_language(self) -> str:
        """Get current language setting."""
        return self.get("ui.language", "en")
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get("logging.level", "INFO")
    
    def is_async_enabled(self) -> bool:
        """Check if async operations are enabled."""
        return self.get("performance.async_operations", True)
    
    def get_window_size(self) -> str:
        """Get window size setting."""
        return self.get("ui.window_size", "1600x800")
    
    def update_language(self, language: str):
        """Update language setting."""
        self.set("ui.language", language)
        self.save_config()
        logger.info(f"Language updated to: {language}")

# Global config instance
config = Config() 