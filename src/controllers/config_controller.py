import json
import os
from src.utils.logger import Logger


class ConfigController:
    logger = Logger()
    
    @staticmethod
    def load_config(config_path='src/config/config.json'):
        try:
            if not os.path.exists(config_path):
                ConfigController.logger.error(f"Config file not found: {config_path}")
                ConfigController.logger.info("Creating default configuration...")
                ConfigController._create_default_config(config_path)
            
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
            
            # Validate required fields
            required_fields = ['scan_folder', 'sub_folders', 'output_folder']
            for field in required_fields:
                if field not in config:
                    raise KeyError(f"Missing required field: {field}")
            
            ConfigController.logger.info("Configuration loaded successfully")
            return config
            
        except json.JSONDecodeError as e:
            ConfigController.logger.error(f"Invalid JSON in config file: {e}")
            raise
        except Exception as e:
            ConfigController.logger.error(f"Error loading config: {e}")
            raise
    
    @staticmethod
    def _create_default_config(config_path):
        default_config = {
            "scan_folder": "scan",
            "sub_folders": ["HN"],
            "output_folder": "output"
        }
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(default_config, file, indent=2)
        
        ConfigController.logger.info(f"Default config created at: {config_path}")
