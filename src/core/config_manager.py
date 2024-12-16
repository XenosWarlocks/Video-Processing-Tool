# proj/src/core/config_manager.py

import os
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
import yaml

class ConfigManager:
    """
    Centralized configuration management with environment-based loading
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_configs(self):
        """Load configurations from YAML files"""
        self.app_config = self._load_yaml('configs/app_config.yaml')
        self.ai_config = self._load_yaml('configs/ai_config.yaml')

    def _load_yaml(self, file_path: str) -> Dict[str, any]:
        """
        Load YAML configuration file
        
        Args:
            file_path (str): Path to the YAML configuration file
        
        Returns:
            Dict[str, Any]: Loaded configuration dictionary
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {file_path}")
            return {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {file_path}: {e}")
            return {}
        
    def get_config(self, config_type: str, key: str, default: None):
        """
        Retrieve a configuration value
        
        Args:
            config_type (str): Type of configuration ('app' or 'ai')
            key (str): Configuration key
            default (Any, optional): Default value if key not found
        
        Returns:
            Any: Configuration value
        """
        config_map = {
            'app': self.app_config,
            'ai': self.ai_config
        }

        return config_map.get(config_type, {}).get(key, default)