import os

from osrparse.replay import Replay
import rosu_pp_py

from constants.paths import PATH_DESCRIPTION_FOLDER_FILES
from model.osu_beatmap import OsuBeatmap
from model.sheet_obr import ColumnSheetObr
from selenium import webdriver

from utils.osu import calculate_acc, get_desc, get_mods

def save_description_obr(browser: webdriver.Firefox, sheet_data: ColumnSheetObr, replay_data: Replay, pp: rosu_pp_py.PerformanceAttributes, map_data: OsuBeatmap, replay_number: int, file_name_as_title: bool = False):
    browser.get(sheet_data["perfil"])
    titulo = browser.title
    nickname = titulo.split(" · ")[0].replace(" ", "_")
    video_title = f"""[{'{:.2f}'.format(pp.difficulty.stars)}⭐] {nickname} | {map_data.song_title} [{map_data.difficulty}] {get_mods(replay_data)} {"{:.2f}".format(calculate_acc(replay_data))}% {get_desc(replay_data, sheet_data)} | {int(pp.pp)}pp"""
    video_description = f"""#OBR #OBR_{nickname}
// Links
Map: {sheet_data["mapa"]}
Skin: {sheet_data["skin"]}
Profile: {sheet_data["perfil"]}
Replay request: https://docs.google.com/forms/d/e/1FAIpQLSdJBj8sHGXrQ4ZarFq2bDDdu4geQwTEu8tg-xJnZzA17QLGXg/viewform
 

Recorded by luis10barbo with danser.
His Profile: https://osu.ppy.sh/users/6405477
Danser: https://github.com/Wieku/danser-go"""
    content = f"""{video_title}
{video_description}"""
    
    file_name = f"{replay_number} - {nickname} {map_data.song_title}".replace("\"", "").replace("'", "").replace("/", "").replace("?", "_").replace(":", "").replace(".", "")

    description_path = os.path.join(PATH_DESCRIPTION_FOLDER_FILES, f"{file_name if file_name_as_title else replay_number}.txt")
    with open(description_path, "w", encoding="utf-8") as file:
        file.write(content)
    
    return file_name