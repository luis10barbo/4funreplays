import os
import json
from unittest.mock import DEFAULT
from lib import *
from lib.paths import MAIN_DIRECTORY, CONFIG_PATH, OUTPUT_DIRECTORY

DEFAULT_CONFIG:dict[str] = {'Directories': {'Main': f"{MAIN_DIRECTORY}", "Osu!": f"{os.path.join(os.getenv('LOCALAPPDATA'), 'osu!')}", 'Danser': '',  'Premiere': '', 'Output': f'{OUTPUT_DIRECTORY}'}}

class ConfigHandler:
    config:dict[str] = {}
    
    def __init__(self) -> None:
        self.check_config()
    
    def save_config(self) -> None:
        logger.info(f"Saving config at path '{CONFIG_PATH}'")
        with open(CONFIG_PATH, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        
    def load_config(self) -> dict[str, dict]:
        logger.info(f"Loading config file at path '{CONFIG_PATH}'")
        
        self.check_config()
        with open(CONFIG_PATH, "r") as file:
            self.config = json.load(file)
        
        self.complete_config()
        
        return self.config

    def generate_config(self):
        # Generate config
        logger.info("Generating config file with default values!")
        self.config = DEFAULT_CONFIG
                
    def complete_config(self):
        # Complete missing keys
        logger.info("Checking if there are missing config options...")
        if self.config == DEFAULT_CONFIG:
            logger.info(f"Current config is equal to default config!")
            return
        
        added_options:int = 0
        
        for key in DEFAULT_CONFIG.keys():
            if key not in self.config:
                added_options += 1
                self.config[key] = DEFAULT_CONFIG[key]
                continue
            for sub_key in DEFAULT_CONFIG[key].keys():
                if sub_key not in self.config[key]:
                    added_options += 1
                    self.config[key] = DEFAULT_CONFIG[key]
                    continue
        
        if added_options != 0:
            logger.info(f"Added {added_options} options to config file!")
            self.save_config()
            return
        logger.info(f"There were no missing config options!")

    def check_config(self):
        if not os.path.isfile(CONFIG_PATH):
            logger.error("Config file does not exist.")
            self.generate_config()
            
        with open(CONFIG_PATH, "r") as file:
            if file.read() == "":
                logger.error("Config file is empty.")
                self.generate_config()