

from logging import info
import os
import subprocess
import time
from typing import Dict
from model.config import get_config
from model.osu_beatmap import OsuBeatmap
from model.osu_db import OsuDb
from utils import buffer
from utils.logger import debug, error
config = get_config()

def read_osu_db():
    with open(os.path.join(config["osu_path"], "osu!.db"), "rb") as db:
        version = buffer.read_uint(db)
        folder_count = buffer.read_uint(db)
        account_unlocked = buffer.read_bool(db)
        # skip this datetime shit for now (8 bytes)
        buffer.read_uint(db)
        buffer.read_uint(db)
        name = buffer.read_string(db)
        num_beatmaps = buffer.read_uint(db)
        beatmaps: Dict[str, OsuBeatmap] = {}
        for _ in range(num_beatmaps):
            artist = buffer.read_string(db)
            artist_unicode = buffer.read_string(db)
            song_title = buffer.read_string(db)
            song_title_unicode = buffer.read_string(db)
            mapper = buffer.read_string(db)
            difficulty = buffer.read_string(db)
            audio_file = buffer.read_string(db)
            md5_hash = buffer.read_string(db)
            map_file = buffer.read_string(db)
            ranked_status = buffer.read_ubyte(db)
            num_hitcircles = buffer.read_ushort(db)
            num_sliders = buffer.read_ushort(db)
            num_spinners = buffer.read_ushort(db)
            last_modified = buffer.read_ulong(db)
            approach_rate = buffer.read_float(db)
            circle_size = buffer.read_float(db)
            hp_drain = buffer.read_float(db)
            overall_difficulty = buffer.read_float(db)
            slider_velocity = buffer.read_double(db)
            # skip these int double pairs, personally i dont think they're 
            # important for the purpose of this database
            i = buffer.read_uint(db)
            for _ in range(i):
                buffer.read_int_float(db)

            i = buffer.read_uint(db)
            for _ in range(i):
                buffer.read_int_float(db)

            i = buffer.read_uint(db)
            for _ in range(i):
                buffer.read_int_float(db)

            i = buffer.read_uint(db)
            for _ in range(i):
                buffer.read_int_float(db)

            drain_time = buffer.read_uint(db)
            total_time = buffer.read_uint(db)
            preview_time = buffer.read_uint(db)
            # skip timing points
            # i = buffer.read_uint(db)
            for _ in range(buffer.read_uint(db)):
                buffer.read_timing_point(db)
            beatmap_id = buffer.read_uint(db)
            beatmap_set_id = buffer.read_uint(db)
            thread_id = buffer.read_uint(db)
            grade_standard = buffer.read_ubyte(db)
            grade_taiko = buffer.read_ubyte(db)
            grade_ctb = buffer.read_ubyte(db)
            grade_mania = buffer.read_ubyte(db)
            local_offset = buffer.read_ushort(db)
            stack_leniency = buffer.read_float(db)
            gameplay_mode = buffer.read_ubyte(db)
            song_source = buffer.read_string(db)
            song_tags = buffer.read_string(db)
            online_offset = buffer.read_ushort(db)
            title_font = buffer.read_string(db)
            is_unplayed = buffer.read_bool(db)
            last_played = buffer.read_ulong(db)
            is_osz2 = buffer.read_bool(db)
            folder_name = buffer.read_string(db)
            last_checked = buffer.read_ulong(db)
            ignore_sounds = buffer.read_bool(db)
            ignore_skin = buffer.read_bool(db)
            disable_storyboard = buffer.read_bool(db)
            disable_video = buffer.read_bool(db)
            visual_override = buffer.read_bool(db)
            last_modified2 = buffer.read_uint(db)
            scroll_speed = buffer.read_ubyte(db)
            beatmaps[md5_hash] = OsuBeatmap(artist, artist_unicode, song_title, song_title_unicode, mapper, difficulty, audio_file, md5_hash, map_file, ranked_status, num_hitcircles, num_sliders, num_spinners, last_modified, approach_rate, circle_size, hp_drain, overall_difficulty, slider_velocity, drain_time, total_time, preview_time, beatmap_id, beatmap_set_id, thread_id, grade_standard, grade_taiko, grade_ctb, grade_mania, local_offset, stack_leniency, gameplay_mode, song_source, song_tags, online_offset, title_font, is_unplayed, last_played, is_osz2, folder_name, last_checked, ignore_sounds, ignore_skin, disable_storyboard, disable_video, visual_override, last_modified2, scroll_speed)
        return OsuDb(version, folder_count, account_unlocked, name, num_beatmaps, beatmaps)

def remove_illegal_characters(string: str):
    string = string.replace(":", "")
    return string

def get_beatmap_difficulty_by_filename(beatmapset_path: str, beatmap_difficulty_name:str):
    return os.path.join(beatmapset_path, beatmap_difficulty_name) 

def get_beatmapset_path_by_folder(beatmap_folder: str):
    return os.path.join(config["osu_path"], "Songs", beatmap_folder) 

def get_beatmapset_path_by_hash(osu_db: OsuDb, beatmap_hash: str):
    return get_beatmapset_path_by_folder(osu_db.beatmaps[beatmap_hash].folder_name) 

def get_beatmap_file_path_by_hash(osu_db: OsuDb, beatmap_hash: str):
    try:
        beatmap = osu_db.beatmaps[beatmap_hash]
    except:
        raise Exception(f"Map {beatmap_hash} not found")
    return get_beatmap_difficulty_by_filename(os.path.join(config["osu_path"], "Songs", beatmap.folder_name), beatmap.map_file) 

def get_beatmapset_path_by_string(target_string: str) -> str | None:
    """
    Search for songs that contain 'target_string' at Songs folder
    """
    debug(
        f"Getting beatmapset that matches string '{target_string}'")

    
    songs_path = os.path.join(config["osu_path"], "Songs")
    folder_content = os.listdir(songs_path)

    # Create list from strings that contain 'song_id' at songs folder
    matching_beatmapsets = [os.path.join(
        songs_path, beatmapset) for beatmapset in folder_content if target_string.lower() in beatmapset.lower()]

    if (len(matching_beatmapsets) is 0):
        error(f"No beatmapset found that matches {target_string}")
        return None
    
    return matching_beatmapsets[0]

def check_if_skin_exists(target_skin: str) -> bool:
    """
    Check if skin 'target_skin' exists at Skins folder.
    """

    info(f"Checking if '{target_skin} exists at osu! folder!'")

    skins_path = os.path.join(config["osu_path"], "Skins")

    folder_content = os.listdir(skins_path)

    if target_skin not in folder_content:
        info("Skin doesn't exist.")
        return False
    info("Skin exists!")
    return True

def get_background_path_from_difficulty(beatmapset_path: str, difficulty_path:str) -> str | None:
    """
    Gets beatmap background of difficulty 'target_dificulty'(without '[]') from beatmapset 'beatmapset_path'
    """
    info(
        f"Getting background from difficulty '{difficulty_path}''")

    with open(difficulty_path, "r", encoding="utf-8") as file:
        difficulty_file = file.read()

    # Try parsing event section
    background: str = ""
    try:
        events_section: list[str] = difficulty_file.split("[Events]")[
            1].split("\n")
        for line in events_section:
            if not line.startswith("0,0,"):
                continue
            background = events_section[2].split(",")[2]
            if background.startswith("\"") and background.endswith("\""):
                background = background[1:][:-1]
            else:
                # TODO: remover essa exception aqui
                raise Exception()
            
    except:
        info("No background found")
        return None
    
    background_path = os.path.join(beatmapset_path, background)
    return background_path

def get_beatmapset_difficulty_by_string(beatmapset_path: str, target_difficulty: str) -> str | None:
    info(
        f"Getting matching difficulty '{target_difficulty}' from beatmapset '{beatmapset_path}'")
    target_difficulty = remove_illegal_characters(target_difficulty)
    matching_files = [os.path.join(beatmapset_path, file) for file in os.listdir(
        beatmapset_path) if "[" + target_difficulty.lower() + "]" in file.lower()]

    if len(matching_files) is 0:
        error(f"No beatmap difficulty found that matches {target_difficulty}")
        return None
    
    return matching_files[0]

def open_beatmap(beatmap_path: str):
    osu = os.path.join(config["osu_path"], "osu!.exe")

    info(f"Opening beatmap {beatmap_path} with osu {osu}")
    subprocess.Popen([f"{osu}", f"{beatmap_path}"])

    time.sleep(15)
    os.system("taskkill /F /IM osu!.exe")

def validate_skin(skin_name: str, skin_link: str = ""):
    # TODO: Create automated skin download
    if skin_name == "Skin Privada ( me mande no privado luis10barbo#3251 )":
        return

    debug(f"Validating skin {skin_name}")
    skins_path = os.path.join(config["osu_path"], "Skins")
    while 1:
        if not skin_name in os.listdir(skins_path):
            error(
                f"Skin {skin_name} not found at osu! skins directory, download it and try again")
            info(
                f"You can download it at {f'{skin_link}' if skin_link != '' else 'No link provided'}")
            input("Press enter after downloading")
            continue
        break

    debug(f"Skin {skin_name} exists at osu! folder")
