import json
import os
import osrparse
import shutil

from lib.paths import OUTPUT_DIRECTORY 

from lib.replays import OsuReplayHandler

OSU_PROFILE_TEMPLATE = "https://osu.ppy.sh/users/"
OSU_BEATMAP_TEMPLATE = "https://osu.ppy.sh/beatmapsets/"

def parse_mods():
    pass

def calculate_accuracy(n300s:int, n100s:int, n50s:int, nmisses:int) -> bool:
    accuracy = "{:0.2f}".format((((50 * n50s) + (100 * n100s) + (300 * n300s)) / (300 * (nmisses + n50s + n100s + n300s))*100))

    return accuracy

def clear_path(file_path:str):
    for file_name in os.listdir(file_path):
        shutil.rmtree(file_name)
        
def clear_folders():
    clear_path(OUTPUT_DIRECTORY)
    

def create_description(output_name:str, user_request:list[dict], beatmap_request:list[dict], star_rating:float, pp:int, skin_link:str, replay_handler:OsuReplayHandler, global_position:int=0):
    beatmap_information = beatmap_request[0]
    title = beatmap_information["title"]
    difficulty = beatmap_information["version"]
    replay_info = replay_handler.replay_info
    
    extensive_mods = replay_handler.replay_info.mod_combination
    mods = (str(replay_info.mod_combination).replace('Mod.', '').replace('|', '').replace("NoMod", "").replace('NoFail', 'NF').replace('NightcoreDoubleTime', 'DT').replace('Nightcore', 'NC').replace('DoubleTime', 'DT').replace('HardRock', 'HR').replace('HalfTime', 'HT').replace('Easy', 'EZ').replace('Flashlight', "FL").replace('Hidden', "HD").replace("DTHD", "HDDT").replace("HRHD", "HDHR"))

    pp_label = ""
    
    accuracy = calculate_accuracy(replay_info.number_300s, replay_info.number_100s, replay_info.number_50s, replay_info.misses)
    
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
    
    is_full_combo:bool = replay_handler.replay_info.max_combo
    
    description = {
        "Title" : f"{nickname} | {star_rating} \U00002B50 | {title} [{difficulty}] +{mods} {accuracy}%{' FC' if is_full_combo else ''}{f' | #{global_position} GLOBAL' if  global_position > 0 else ''}",
        "Description" : f"""#osu #osu4fun #osu4fun_{nickname.replace(' ', '_').replace('-', '_')} \n
Gravado usando danser-go :)\n
Baixe aqui:https://github.com/Wieku/danser-go\n
Mande sua play aqui:discord.gg/WdwcX9Z\n
(Leia o pin antes de mandar plays)\n\n
Jogador: {osu_profile_link}\n
Mapa: {beatmap_profile_link}\n
Skin: {skin_link}""",
        "Tags": f"""osu!4fun,osu!,4fun,br,osu! 4FunBR,Replays,4FunBR,
{nickname},
{str(nickname).replace(" ", "")}, {mods},
{str(extensive_mods).replace("|", ",")}, {str(int(float(star_rating)))}*
{str(int(float(pp) / 100) * 100) + pp_label}pp"""
    }
    
    output = os.path.join(OUTPUT_DIRECTORY, f"{output_name}.json")
    with open(output, "w") as file:
        json.dump(description, file, indent=4)