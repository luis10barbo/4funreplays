import pickle
import requests
import os

import lib
from lib import logger

MAIN_PATH = os.getcwd()
OSU_BEATMAPS_DOWNLOAD_PATH = os.path.join(MAIN_PATH, "downloads", "beatmaps")
OSU_SECRETS_PATH = os.path.join(MAIN_PATH, "secrets", "osu")
OSU_CREDENTIALS_PATH = os.path.join(OSU_SECRETS_PATH, 'credentials.txt')
OSU_SESSION_PATH = os.path.join(OSU_SECRETS_PATH, 'session')

OSU_HOMEPAGE_URL = "https://osu.ppy.sh/home"
OSU_SESSION_URL = "https://osu.ppy.sh/session"
OSU_BEATMAPSETS_URL = "https://osu.ppy.sh/beatmapsets/"
osu_beatmapset_url = ""
DOWNLOAD_PATH = ""
OSU_REPLAY_URL = "https://osu.ppy.sh/scores/mania/485188165"


class OsuSessionHandler:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.load_session()
        
        self.logged_in = False
        self.login()
        
        self.save_session()
    
    def save_session(self) -> None:
        with open(OSU_SESSION_PATH, "wb") as file:
            pickle.dump(self.session, file)
            
    def load_session(self) -> None:
        if os.path.isfile(OSU_SESSION_PATH) == False:
            logger.error(f"No osu session found at {OSU_SESSION_PATH}")
            return
        
        with open(OSU_SESSION_PATH, "rb") as file:
            self.session = pickle.load(file)
            
    def save_html(self, raw_html) -> None:
        with open("osu_page.html", "w", encoding="utf-8") as file:
            file.write(raw_html)
            
    def get_token(self) -> None:
        response = self.session.get(OSU_HOMEPAGE_URL)
        # self.save_html(response.text)
        
        html_split = response.text.split('<input name="_token" type="hidden" value="', 1)
        if len(html_split) == 1:
            self.logged_in = True
            return
        else:
            self.token = html_split[1].split('"', 1)[0]
            
    def get_credentials_from_file(self) -> None:
        with open(OSU_CREDENTIALS_PATH, "r") as file:
            credentials = file.read().split("\n")

        username = credentials[0]
        password = credentials[1]
        return username, password
            
    def login(self, from_file=False) -> None:
        self.get_token()
        if self.logged_in == True:
            logger.info("Logged in at osu!")
            return
        
        if from_file:
            username, password = self.get_credentials_from_file()
        else:
            username = lib.prompt.string("Type here your osu! username")
            password = lib.prompt.password("Type here your osu! password")
        data = {"_token": self.token,"username": username, "password" : password}
        headers = {"referer": OSU_HOMEPAGE_URL}
        
        response = self.session.post(url=OSU_SESSION_URL, data=data, headers=headers)
        if response.status_code == 200:
            logger.info("Logged in at osu!")

    def write_file(self, file_path:str, data) -> None:
        with open(file_path, "wb") as file:
            file.write(data)
        
    def download_beatmap(self, beatmapset_url, file_name) -> None:
        output_path = os.path.join(OSU_BEATMAPS_DOWNLOAD_PATH, file_name)
        
        download_url = f"{beatmapset_url}/download?noVideo=1" 
        
        headers = {"referer": beatmapset_url}
        
        logger.info(f"Downloading Beatmap from {download_url}")
        response = self.session.get(download_url, headers=headers)

        if response.status_code == requests.codes.ok:
            logger.info("Download Sucessful")
            self.write_file(file_path=output_path, data=response.content)
            return output_path
            
    def download_replay(self, replay_url:str, file_path:str):
        return logger.info(f"NOT WORKING YET {__name__}")
        headers = {"referer": OSU_REPLAY_URL}
        download_url = f"{OSU_REPLAY_URL}/download"
        
        response = self.session.get(download_url, headers=headers)
        if response.status_code == requests.codes.ok:
            logger.info("Replay download sucessful!")
            self.write_file("replay.osr", response.content)