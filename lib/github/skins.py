import json
import requests
from lib import logger
import os

from lib.paths import SKINS_FILE

def parse_github_skins(github_text:str) -> dict:
    lines = github_text.split("\n")
    skins = {}
    for i in range(len(lines)):
            current_line : str = lines [i]
            if current_line.startswith("#") == True:
                skin_name = current_line.split("[", 1)[1].rsplit("]", 1)[0]
                skin_link = f"h{current_line.rsplit('(h', 1)[1].rsplit(')', 1)[0]}"
                
                skins[skin_name] = {"link" : skin_link}
    
    return skins

class SkinHandler:
    skins_link = "https://raw.githubusercontent.com/luis10barbo/osu4fun-skins/main/README.md"
    skins = {}

    def __init__(self) -> None:
        self.get_skins_local()
        
    def verify_local_skins(self):
        if not os.path.isfile(SKINS_FILE):
            self.save_skins({})
            
    def save_skins(self, skins:dict[str, str]):  
        logger.debug(f"Saving skins to local skin files at {SKINS_FILE}")  
        with open(SKINS_FILE, "w") as file:
            json.dump(skins, file, indent=4) 
    
    def get_skins_local(self):
        self.verify_local_skins()
        logger.debug(f"Getting local skin files from {SKINS_FILE}")
        with open(SKINS_FILE, "r") as file:
            file_text = file.read()
            if file_text == "":
                self.skins = {}
            else:
                self.skins = json.loads(file_text)
        
    def get_skins_from_github(self) -> None:
        response = requests.get(self.skins_link)
        skins = parse_github_skins(response.text)
        self.save_skins(skins)
        
        self.skins = skins

    def get_skin_by_name(self, target_skin:str) -> None:
        self.get_skins_local()
        if target_skin in self.skins:
            return self.skins[target_skin]   
        logger.error(f"No skin matching to '{target_skin}' found at local skins, making github request")

        self.get_skins_from_github()
        if target_skin in self.skins:
            return self.skins[target_skin]
        logger.error(f"No skin matching to '{target_skin}' found at github skins", True)
        input("Press enter after adding skin to github")


            
        
       