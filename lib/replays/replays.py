import os
import lib

import osrparse

REPLAYS_DIRECTORY = os.path.join(os.getcwd(), "downloads", "replays")

def download_replay(file_url:str, file_name:str):
    return lib.google.drive.download_from_drive(file_url, REPLAYS_DIRECTORY, file_name)
    
class OsuReplayHandler():    
    replay_path = ""
    replay_info:osrparse.Replay
    
    def __init__(self, queue_entry:dict) -> None:
        self.get_replay_from_queue(queue_entry)
        self.parse_replay()
        
    def get_replay_from_queue(self, queue_entry:dict):
        self.replay_path = os.path.join(REPLAYS_DIRECTORY, f"{queue_entry['replay_id']}.osr") 

    def parse_replay(self):
        self.replay_info = osrparse.parse_replay_file(self.replay_path)