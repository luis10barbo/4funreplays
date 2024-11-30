
import os
from typing import Any
import requests
from utils.logger import error, debug, warn

from constants.paths import PATH_OSU_BEATMAPS_DOWNLOADS

OSU_HOMEPAGE_URL = "https://osu.ppy.sh/home"
OSU_SESSION_URL = "https://osu.ppy.sh/session"
OSU_BEATMAPSETS_URL = "https://osu.ppy.sh/beatmapsets/"
osu_beatmapset_url = ""
DOWNLOAD_PATH = ""
OSU_REPLAY_URL = "https://osu.ppy.sh/scores/mania/485188165"

# def get_session() -> requests.Session:
#         session = load_session_from_file()
#         if session == None:
#             session = requests.Session()

#         session = try_login(session)
        
#         save_session(session)
#         return session
    
# def save_session(session: requests.Session) -> None:
#     with open(PATH_OSU_SESSION, "wb") as file:
#         pickle.dump(session, file)
        
# def load_session_from_file() -> requests.Session | None:
#     if os.path.isfile(PATH_OSU_SESSION) == False:
#         error(f"No osu session found at {PATH_OSU_SESSION}")
#         return
    
#     with open(PATH_OSU_SESSION, "rb") as file:
#         session: requests.Session = pickle.load(file)
#     return session
        

# def get_token(session: requests.Session) -> None | str:
#     response = session.get(OSU_HOMEPAGE_URL)
#     # self.save_html(response.text)
    
#     html_split = response.text.split('<input name="_token" type="hidden" value="', 1)
#     if len(html_split) == 1:
#         return None
#     else:
#         return html_split[1].split('"', 1)[0]
    
        
# def try_login(session: requests.Session) -> requests.Session:
#     token = get_token(session)
#     if token == None:
#         debug("Already logged in")
#         return session

#     username = input("Type here your osu! username")
#     password = input("Type here your osu! password")

#     data: dict[str, str] = {"_token": token,"username": username, "password" : password}
#     headers = {"referer": OSU_HOMEPAGE_URL}
    
#     response = session.post(url=OSU_SESSION_URL, data=data, headers=headers)
#     if response.status_code == 200:
#         debug("Logged in at osu!")
#     return session

def write_file(file_path:str, data: Any) -> None:
    with open(file_path, "wb") as file:
        file.write(data)
    
def download_beatmap(beatmapset_url:str, file_name:str) -> str:
    output_path = os.path.join(PATH_OSU_BEATMAPS_DOWNLOADS, file_name)
    
    # Check if beatmapset url is a redirect
    response = requests.get(beatmapset_url, allow_redirects=True)
    if response.status_code == requests.codes.found:
        debug(f"Beatmap link redirect from {beatmapset_url} to {response.url}")
        beatmapset_url = response.url

    # download_url = f"{beatmapset_url}/download?noVideo=1" 
    
    # headers = {"referer": beatmapset_url}
    
    # debug(f"Downloading Beatmap from {download_url} to {output_path}")
    # response = session.get(download_url, headers=headers)

    # if response.status_code == requests.codes.ok:
    #     debug("Beatmap download Sucessful")
    #     write_file(file_path=output_path, data=response.content)
    #     return output_path
    beatmapset_id = beatmapset_url.rsplit("#osu", 1)[0].rsplit("/", 1)[1].replace('/', '')
    download_url = f"https://api.nerinyan.moe/d/{beatmapset_id}?noVideo=true&NoStoryboard=true"
    warn(f"Using mirror to download beatmap {download_url}")

    response = requests.get(download_url)
    if response.status_code == requests.codes.ok:
        debug("Download Sucessful")
        write_file(file_path=output_path, data=response.content)
        return output_path
    else:
        error("Error downloading")
        debug(str(response.headers))
    return output_path

        
# def download_replay(replay_url:str, file_path:str):
#     return logger.info(f"NOT WORKING YET {__name__}")
#     headers = {"referer": OSU_REPLAY_URL}
#     download_url = f"{OSU_REPLAY_URL}/download"
    
#     response = self.session.get(download_url, headers=headers)
#     if response.status_code == requests.codes.ok:
#         logger.info("Replay download sucessful!")
#         self.write_file("replay.osr", response.content)