import json
import os
from constants.paths import PATH_CONFIG_FILE
from typing import TypedDict 
from tkinter import Tk, filedialog
from utils.logger import debug, error

from utils.arguments_parser import parse_arguments
class Config(TypedDict):
    osu_path: str
    danser_path: str
    danser_config: str
    premiere_path: str

def get_config():
    debug("Getting config")

    args = parse_arguments()
    config: Config | None
    if args.new_cfg is True:
        config = create_config()
    else:
        config = read_config()

    if config is None:
        error("No config found")
        raise Exception("No config found")
    
    return config
    

def read_config():
    config: Config | None
    try:
        with open(PATH_CONFIG_FILE, "+r") as config_file:
            config_contents = config_file.read()
            config = json.loads(config_contents)
            debug("Getting config from file")
            if config:
                debug(f"Config loaded {json.dumps(config)}")
            return config
    except:
        pass
    config = create_config()
    if config is None:
        return None
    
    return config

def save_config(config: Config):
    with open(PATH_CONFIG_FILE, "w") as config_file:
        debug("Saving config")
        json.dump(config, config_file)

def create_config() -> Config | None:
    root = Tk()
    root.withdraw()
    debug("Creating new config")
    
    osu_dir = ""
    # Get osu folder 
    while True:
        osu_dir = filedialog.askdirectory(title="Select osu directory", initialdir="%localappdata%")
        if not osu_dir:
            return None
        
        files_in_folder = os.listdir(osu_dir)
        if "osu!.exe" in files_in_folder:
            break

        error(f"osu.exe not found in folder, files in folder: {files_in_folder}")
    
    danser_dir = ""
    # Get danser folder 
    while True:
        danser_dir = filedialog.askdirectory(title="Select danser directory")
        if not danser_dir:
            return None
        
        files_in_folder = os.listdir(danser_dir)
        if "danser-cli.exe" in files_in_folder:
            break

        error(f"danser-cli.exe not found in folder, files in folder: {files_in_folder}")
    
    danser_config_path = filedialog.askopenfile(initialdir=os.path.join(danser_dir, "settings"), filetypes=[("Settings Files", "*.json")], title="Select danser config")
    if danser_config_path is None or type(danser_config_path.name) is not str:
        return None
    
    danser_config = os.path.basename(danser_config_path.name).replace(".json", "").strip()
    config = Config(danser_path=danser_dir, danser_config=danser_config, osu_path=osu_dir, premiere_path=r"C:\Program Files\Adobe\Adobe Premiere Pro 2021\Adobe Premiere Pro.exe")
    save_config(config)
    return config
