import json
import os
import logging
from datetime import datetime

class ConfigLoader:
    def __init__(self, config_file='config/settings.json'):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config = self.load_default_config()
        self.load()
    
    def load_default_config(self):
        """Return default configuration"""
        return {
            "version": "2.0.0",
            "ai_settings": {
                "learning_enabled": True,
                "threat_detection": True,
                "optimization_enabled": True,
                "model_retrain_interval": 24
            },
            "storage": {
                "default_locations": {
                    "servers": "data/servers",
                    "backups": "data/backups",
                    "logs": "data/logs",
                    "temp": "data/temp"
                },
                "auto_cleanup": True,
                "cleanup_interval": 7
            },
            "servers": {
                "default_ports": {
                    "http": 8080,
                    "https": 8443,
                    "tcp": 9000,
                    "udp": 9001
                },
                "auto_start": False,
                "max_instances": 5
            },
            "applications": {
                "auto_import": True,
                "launch_delay": 2,
                "monitor_resources": True
            },
            "ui": {
                "theme": "dark",
                "auto_save": True,
                "refresh_interval": 10
            }
        }
    
    def load(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self._merge_configs(loaded_config)
                self.logger.info("Configuration loaded successfully")
            else:
                self.logger.info("No config file found, using defaults")
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def _merge_configs(self, new_config):
        """Merge loaded config with defaults"""
        def merge_dicts(default, new):
            for key, value in new.items():
                if key in default:
                    if isinstance(default[key], dict) and isinstance(value, dict):
                        merge_dicts(default[key], value)
                    else:
                        default[key] = value
            return default
        
        self.config = merge_dicts(self.config, new_config)
    
    def get(self, key, default=None):
        """Get configuration value by dot notation key"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Set configuration value by dot notation key"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()