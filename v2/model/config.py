import json
import os
from constants.paths import PATH_CONFIG_FILE
from typing import TypedDict 
from tkinter import Tk, filedialog

from utils.arguments_parser import parse_arguments
class Config(TypedDict):
    danser_path: str
    danser_config: str

def get_config():
    args = parse_arguments() 
    if args.new_cfg is True:
        return create_config()
    else:
        return read_config()
    

def read_config():
    config: Config | None
    try:
        with open(PATH_CONFIG_FILE, "+r") as config_file:
            config_contents = config_file.read()
            config = json.loads(config_contents)
            return config
    except:
        pass
    config = create_config()
    if config is None:
        return None
    
    return config

def save_config(config: Config):
    with open(PATH_CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)

def create_config() -> Config | None:
    root = Tk()
    root.withdraw()

    danser_dir = filedialog.askdirectory(title="Select danser directory")
    if not danser_dir:
        return None
    
    danser_config_path = filedialog.askopenfile(initialdir=os.path.join(danser_dir, "settings"), filetypes=[("Settings Files", "*.json")], title="Select danser config")
    if danser_config_path is None or type(danser_config_path.name) is not str:
        return None
    
    danser_config = os.path.basename(danser_config_path.name).replace(".json", "").strip()
    config = Config(danser_path=danser_dir, danser_config=danser_config)
    save_config(config)
    return config
