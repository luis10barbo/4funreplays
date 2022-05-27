import subprocess
import json
import os
import lib
from lib import logger

DANSER_EXECUTABLE = "danser.exe"
DEFAULT_SETTINGS = "teste2lb"

def get_from_range(number:float, smallest_number:float, largest_number:float):
    # Clamp
    print(number, largest_number, smallest_number)
    print(type(number), type(largest_number), type(smallest_number))
    return max(smallest_number, min(number, largest_number))

class OsuDanserHandler():
    danser_path = ""
    is_valid_path = False
    
    def __init__(self, config:dict={}) -> None:
        if config != {}:
            self.load_path_from_config(config)
    
    def verify_danser_path(self) -> bool:
        if not os.path.isdir(self.danser_path):
            logger.error("Specified danser path is not a valid path")
            self.is_valid_path = False
            return
        
        if not DANSER_EXECUTABLE in os.listdir(self.danser_path):
            logger.error(f"Danser executable '{DANSER_EXECUTABLE}' not found at {self.danser_path}")
            self.is_valid_path = False
            return
        
        logger.info("Danser path is valid")
        self.is_valid_path = True
    
    def load_path_from_config(self, config:dict):
        self.danser_path = config["Directories"]["Danser"]
        if self.danser_path == "":
            logger.error("Danser path at config file is empty!")
            return
        
        self.verify_danser_path()
    
    def validate_setting(self, template_setting:str):
        if self.is_valid_path == False:
            logger.error("Danser path is not valid")
            return
        
        SETTINGS_PATH = os.path.join(self.danser_path, "settings")
        
        if not os.path.isdir(SETTINGS_PATH):
            logger.error("No 'settings' folder at danser folder, make sure you're using danser 6.0+ and runned it at least once")
            return
            
        SETTING_PATH = os.path.join(SETTINGS_PATH, f"{template_setting}.json") 
        
        if not os.path.isfile(SETTING_PATH):
            logger.error(f"No '{template_setting}.json' setting found at '{SETTINGS_PATH}'")
            return
    
    def create_setting_file(self, setting, setting_name = "customconfig"):
        SETTING_PATH = os.path.join(self.danser_path, "settings", f"{setting_name}.json")
        
        with open(SETTING_PATH, "w", encoding="utf-8") as file:
            json.dump(setting, file, indent=4)
        logger.info(f"Created danser setting at '{SETTING_PATH}'")
        
        return setting_name

        
    def setup_custom_settings(self, template_setting:str=DEFAULT_SETTINGS, cursor_size:float=1.0):
        # Validate settings
        if self.validate_setting(template_setting) == False:
            logger.info("Custom settings won't be created.")
            return
        
        SETTINGS_PATH = os.path.join(self.danser_path, "settings")
        TEMPLATE_SETTING_PATH = os.path.join(SETTINGS_PATH, f"{template_setting}.json") 
        
        with open(TEMPLATE_SETTING_PATH, "r", encoding="utf-8") as file:
            custom_setting = json.load(file)
        
        # cursor size
        custom_setting["Skin"]["Cursor"]["Scale"] = get_from_range(cursor_size, 0.1, 2.0)
            
        return custom_setting
        
    def record_replay(self, replay_path:str, skin_name:str, video_name:str, video_prefix="", setting_name="teste2lb", custom_setting:dict={}) -> str:
        if self.is_valid_path == False:
            logger.error("Danser path is not valid, replay won't be recorded")
        
        if type(custom_setting) == dict:
            if custom_setting != {}:
                setting_name = self.create_setting_file(custom_setting)
            
        danser_arguments = (f'danser.exe -skip -replay "{replay_path}" -skin "{skin_name}" -settings="{setting_name}"')
        
        executable_path = os.path.join(self.danser_path, "4funreplays.bat")
        with open(executable_path, "w") as file:
            file.write(danser_arguments)
        
        subprocess.run(f"{executable_path}", cwd=self.danser_path)
        
        return os.path.join(self.danser_path, "videos", f"{video_name}.mp4")
        
        