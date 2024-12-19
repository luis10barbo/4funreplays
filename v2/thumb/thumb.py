import os
import time
import urllib.parse
from osrparse.replay import Replay
import rosu_pp_py
from selenium import webdriver
import urllib

from constants.paths import PATH_OBR_THUMB_FILE, PATH_THUMB_FOLDER_FILES
from model.osu_beatmap import OsuBeatmap
from model.sheet_obr import ColumnSheetObr
from osu.local.folder import get_background_path_from_difficulty, get_beatmapset_path_by_folder, get_beatmap_difficulty_by_filename
from osu.web.osu_web import get_pfp_url
from utils import logger
from utils.logger import debug
from utils.osu import calculate_acc, calculate_grade, get_desc, get_mods

def save_thumbnail_obr(browser: webdriver.Firefox, sheet_data: ColumnSheetObr, replay_data: Replay, pp_data: rosu_pp_py.PerformanceAttributes, map_data: OsuBeatmap, index: int, video_title: str | None): 
    
    bg = get_background_path_from_difficulty(
                    beatmapset_path=get_beatmapset_path_by_folder(map_data.folder_name), difficulty_path=get_beatmap_difficulty_by_filename(get_beatmapset_path_by_folder(map_data.folder_name), beatmap_difficulty_name=map_data.map_file)
                    )
    
    
    if not bg:
        logger.error("No bg found")
        return
    
    bg = bg.replace("\\", "\\\\").replace("/", "\\\\")
    
    url = f"file:///{PATH_OBR_THUMB_FILE}\
?mapa={urllib.parse.quote(map_data.song_title)}\
&nickname={replay_data.username}\
&obs={urllib.parse.quote(sheet_data["o_que_seria"].encode("utf-8"))}\
&acc={"{:.2f}".format(calculate_acc(replay_data))}%\
&mods={get_mods(replay_data)}\
&pp={round(pp_data.pp)}pp\
&combo={replay_data.max_combo}x\
&sr={"{:.2f}".format(pp_data.difficulty.stars)} ⭐\
&diff=[{urllib.parse.quote(map_data.difficulty)}]\
&bg={bg}\
&pfp={get_pfp_url(sheet_data["perfil"])}\
&grade={calculate_grade(replay_data)}\
&desc={get_desc(replay_data, sheet_data)}"
    debug(f"Opening thumbnail with url \"{url}\"")
    browser.get(url)
    screenshot_path = os.path.join(PATH_THUMB_FOLDER_FILES, f"{video_title if video_title else index}.png")
    time.sleep(2)
    browser.save_screenshot(screenshot_path) # type: ignore
    debug(f"Screenshot saved at {screenshot_path}")
