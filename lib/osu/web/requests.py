import json
import os
import shutil
import lib
from lib import logger

import osrparse

import requests

from lib.paths import SECRETS_PATH, API_PATH, OSU_SECRETS_PATH

REQUEST_FOLDER = os.path.join(os.getcwd(), "info", "requests")

class OsuRequestHandler():
    api = ""
    parsed_replay = None
    queue_entry = []
    
    beatmap_info = []
    beatmap_scores = []
    player_info = []
    
    has_updated_spreadsheet = False
    
    def __init__(self, queue_information:dict[str,str], replay_information:osrparse.Replay, has_updated_spreadsheet:bool=True) -> None:
        self.get_api_from_secrets()

        if has_updated_spreadsheet == True:
            self.has_updated_spreadsheet = True
            
        self.set_queue_information(queue_information)
        self.set_replay_information(replay_information)
        
    def check_api(self):
        if not os.path.isfile(API_PATH):
            logger.error(f"No api file found at {API_PATH}")
            return
                
        if self.api == "":
            logger.error(f"No api key found at {API_PATH}.")
            return
        
    def clear_request_folder(self, clear_folder:bool = True):
        if clear_folder == False:
            logger.info("Variable 'clear_folder' set to False, requests folder wont be cleared.")
            return
        logger.info(f"Removing all requests in {REQUEST_FOLDER} folder...")
        request_folders = [os.path.join(REQUEST_FOLDER, folder_name) for folder_name in os.listdir(REQUEST_FOLDER)]
        for folder_path in request_folders:
            shutil.rmtree(folder_path)
            logger.debug(f"Removed {folder_path}.")

        
    def get_api_from_secrets(self):
        with open(API_PATH, "r") as file:
            self.api = file.read()
            
        self.check_api()

    def set_replay_information(self, replay_information:osrparse.Replay):
        self.parsed_replay:osrparse.Replay = replay_information

    def set_queue_information(self, queue_entry:dict[str,str]):
        self.queue_entry : dict[str,str] = queue_entry
        self.create_folder()
        
    def create_folder(self):
        current_entry_path = os.path.join(REQUEST_FOLDER, f"{self.queue_entry['replay_id']}")
        
        if not os.path.isdir(current_entry_path):
            logger.info(f"Folder {current_entry_path} doesn't exist, creating it.")
            os.mkdir(current_entry_path)
        
    def save_request(self, request_name:str, request_json):
        current_entry_path = os.path.join(REQUEST_FOLDER, f"{self.queue_entry['replay_id']}")
        
        if not os.path.isdir(current_entry_path):
            logger.info(f"Folder {current_entry_path} doesn't exist, creating it.")
            os.mkdir(current_entry_path)
        
        request_output = os.path.join(current_entry_path, f'{request_name}.json')
        
        with open(request_output, "w") as file:
            json.dump(request_json, file, indent=4)
    
    def open_request(self, request_name:str) -> list:
        request_output = os.path.join(REQUEST_FOLDER, f"{self.queue_entry['replay_id']}", f'{request_name}.json')

        if not os.path.isfile(request_output):
            logger.error(f"No request file found at {request_output}")

        with open(request_output, "r") as file:
            request = json.load(file)
        
        return request

    def should_make_request(self, REQUEST_NAME:str) -> bool:
        output_path = os.path.join(REQUEST_FOLDER, f"{self.queue_entry['replay_id']}", f"{REQUEST_NAME}.json")
        return (self.has_updated_spreadsheet == False) and (os.path.isfile(output_path) == False)

    def get_beatmap(self):
        self.check_api()

        REQUEST_URL = "https://osu.ppy.sh/api/get_beatmaps?"
        REQUEST_NAME = "beatmap_info"

        sucess = False
        if self.should_make_request(REQUEST_NAME) == False:
            self.beatmap_info = self.open_request(REQUEST_NAME)
            logger.debug("Queue has not been updated, ignoring beatmap request")
            return

        if self.parsed_replay != None:
            # First check
            beatmap_hash = self.parsed_replay.beatmap_hash
            logger.info(f"Requesting beatmap information from beatmap with hash {beatmap_hash}")

            self.beatmap_info = json.loads(requests.get(url=REQUEST_URL, params={"k":self.api, "h":beatmap_hash}).text)
            
            sucess = True if self.beatmap_info != [] else False
        
        if self.queue_entry != [] and sucess == False:
            # Second check
            beatmap_id = self.queue_entry["map"].split("#osu/")[1]
            logger.info(f"Requesting beatmap information from beatmap with id {beatmap_id}")
            
            self.beatmap_info = json.loads(requests.get(url=REQUEST_URL, params={"k":self.api, "h":beatmap_id}).text)
            
            sucess = True if self.beatmap_info != [] else False
            
        if sucess == False:
            logger.error("Beatmap requests have been unsucessful")
            return
        
        self.save_request(REQUEST_NAME, self.beatmap_info)
            
    def get_scores(self):
        self.check_api()

        REQUEST_URL = "https://osu.ppy.sh/api/get_scores?"
        REQUEST_NAME = "beatmap_scores"

        sucess = False
            
        if self.should_make_request(REQUEST_NAME) == False:
            self.beatmap_scores = self.open_request(REQUEST_NAME)
            logger.debug("Queue has not been updated, ignoring beatmap scores request")
            return
            
        if self.parsed_replay != None:
            # First check
            beatmap_id = self.queue_entry["map"].split("#osu/")[1]
            logger.info(f"Requesting beatmap scores from beatmap with id {beatmap_id}")

            self.beatmap_scores = json.loads(requests.get(url=REQUEST_URL, params={"k":self.api, "b":beatmap_id}).text)
            
            sucess = True if self.beatmap_scores != [] else False
            
        if sucess == False:
            logger.error("Score requests have been unsucessful")
            return
        
        self.save_request(REQUEST_NAME, self.beatmap_scores)

    def get_player_info(self):
        self.check_api()

        REQUEST_URL = "https://osu.ppy.sh/api/get_user?"
        REQUEST_NAME = "player_info"

        self.player_info = []
        if self.should_make_request(REQUEST_NAME) == False:
            self.player_info = self.open_request(REQUEST_NAME)
            logger.debug("Queue has not been updated, ignoring player info request")
            return
        
        if self.parsed_replay != None:
            # First check
            user_id = self.queue_entry["profile"].split("users/")[1]
            logger.info(f"Requesting user information from user with id {user_id}")

            self.player_info = json.loads(requests.get(url=REQUEST_URL, params={"k":self.api, "u":user_id}).text)
            
            sucess = True if self.player_info != [] else False
            
        if sucess == False:
            logger.error("User info requests have been unsucessful")
            return
        
        self.save_request(REQUEST_NAME, self.player_info)
        

