# proj/src/core/base_processor.py

import os
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
import yaml

from src.core.config_manager import ConfigManager

class BaseProcessor(ABC):
    """
    Abstract base class for all processors in the video processing pipeline
    """
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize processor with configuration management
        
        Args:
            config_manager (ConfigManager): Centralized configuration manager
        """
        self.config = config_manager
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logging for the processor
        
        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(f'logs/{self.__class__.__name__}.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        logger.addHandler(file_handler)
        return logger
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Abstract method to be implemented by child classes
        
        Args:
            input_data (Any): Input data to be processed
        
        Returns:
            Any: Processed output
        """
        pass

    def log_error(self, message: str):
        """
        Log error messages
        
        Args:
            message (str): Error message to log
        """
        self.logger.error(message)
    
    def log_info(self, message: str):
        """
        Log informational messages
        
        Args:
            message (str): Information message to log
        """
        self.logger.info(message)