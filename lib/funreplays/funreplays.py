import json
import os
import osrparse
import shutil

import lib.osu

from lib.paths import OUTPUT_DIRECTORY, REQUEST_FOLDER, REPLAYS_DOWNLOAD_PATH, BEATMAPS_DOWNLOAD_PATH

from lib.replays import OsuReplayHandler

OSU_PROFILE_TEMPLATE = "https://osu.ppy.sh/users/"
OSU_BEATMAP_TEMPLATE = "https://osu.ppy.sh/beatmapsets/"

def parse_mods():
    pass

def clear_path(target_path:str):
    for file_name in os.listdir(target_path):
        file_path = os.path.join(target_path, file_name)
        if os.path.isdir(file_path) == True:
            shutil.rmtree(os.path.join(target_path, file_name))
        else:
            os.remove(file_path)
        
def clear_folders():
    clear_path(OUTPUT_DIRECTORY)
    clear_path(REQUEST_FOLDER)
    clear_path(REPLAYS_DOWNLOAD_PATH)
    clear_path(BEATMAPS_DOWNLOAD_PATH)
    

def create_description(output_name:str, user_request:list[dict], beatmap_request:list[dict], star_rating:float, pp:int, skin_link:str, replay_handler:OsuReplayHandler, global_position:int=0):
    beatmap_information = beatmap_request[0]
    title = beatmap_information["title"]
    difficulty = beatmap_information["version"]
    replay_info = replay_handler.replay_info
    
    extensive_mods = replay_handler.replay_info.mod_combination
    mods = (str(replay_info.mod_combination).replace('Mod.', '').replace('|', '').replace("NoMod", "").replace('NoFail', 'NF').replace('NightcoreDoubleTime', 'DT').replace('Nightcore', 'NC').replace('DoubleTime', 'DT').replace('HardRock', 'HR').replace('HalfTime', 'HT').replace('Easy', 'EZ').replace('Flashlight', "FL").replace('Hidden', "HD").replace("DTHD", "HDDT").replace("HRHD", "HDHR"))

    pp_label = ""
    
    accuracy = lib.osu.calculate_accuracy(replay_info.number_300s, replay_info.number_100s, replay_info.number_50s, replay_info.misses)
    
    user_information = user_request[0]
    mode = "#osu"
    match(beatmap_information['mode']):
        case 0:
            mode = "#osu"
        case 1:
            mode = "#taiko"
        case 2:
            mode = "#fruits"
        case 3:
            mode = "#mania"
    
    nickname = f"{user_information['username']}"
    osu_profile_link = f"{OSU_PROFILE_TEMPLATE}{user_information['user_id']}"
    beatmap_profile_link = f"{OSU_BEATMAP_TEMPLATE}{beatmap_information['beatmapset_id']}{mode}/{beatmap_information['beatmap_id']}"
    
    is_full_combo:bool = replay_handler.replay_info.is_perfect_combo
    
    description = {
        "Title" : f"{nickname} | {star_rating}\U00002B50 | {title} [{difficulty}] {f'+{mods}' if len(mods) > 0 else ''} {accuracy}%{' FC' if is_full_combo else ''}{f' | #{global_position} GLOBAL' if  global_position > 0 else ''}",
        "Description" : f"""#osu #osu4fun #osu4fun_{nickname.replace(' ', '_').replace('-', '_')}
Gravado usando danser-go :)
Baixe aqui:https://github.com/Wieku/danser-go
Mande sua play aqui:discord.gg/WdwcX9Z
(Leia o pin antes de mandar plays)

Jogador: {osu_profile_link}
Mapa: {beatmap_profile_link}
Skin: {skin_link}""",
        "Tags": f"""osu!4fun,osu!,4fun,br,osu! 4FunBR,Replays,4FunBR,
{nickname},
{str(nickname).replace(" ", "")}, {mods},
{str(extensive_mods).replace("|", ",")}, {str(int(float(star_rating)))}*
{str(int(float(pp) / 100) * 100) + pp_label}pp"""
    }
    
    output = os.path.join(OUTPUT_DIRECTORY, f"{output_name}.txt")
    with open(output, "w", encoding="utf-8") as file:
        file.write(description["Title"] + "\n")
        file.write(description["Description"] + "\n")
        file.write(description["Tags"] + "\n")