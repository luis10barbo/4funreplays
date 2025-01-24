from typing import cast
from osrparse.replay import Replay
from osrparse.utils import Mod

from model.sheet_obr import ColumnSheetObr


def calculate_acc(replay_data: Replay):
    return (((300 * replay_data.count_300) + (100 * replay_data.count_100) + (50 *replay_data.count_50)) / (300 * (replay_data.count_300 + replay_data.count_100 + replay_data.count_50 + replay_data.count_miss))) * 100

def get_mods(replay_data: Replay):
    mods = [cast(str, mod.name) for mod in Mod if replay_data.mods & mod] #type:ignore
    mods_simplified = {
        'NoMod': 'NM',
        'NoFail': 'NF',
        'Easy': 'EZ',
        'TouchDevice': 'TD',
        'Hidden': 'HD',
        'HardRock': 'HR',
        'SuddenDeath': 'SD',
        'DoubleTime': 'DT',
        'Relax': 'RX',
        'HalfTime': 'HT',
        'Nightcore': 'NC',
        'Flashlight': 'FL',
        'Autoplay': 'AP',
        'SpunOut': 'SO',
        'Autopilot': 'AT',
        'Perfect': 'PF',
        'Key4': 'K4',
        'Key5': 'K5',
        'Key6': 'K6',
        'Key7': 'K7',
        'Key8': 'K8',
        'FadeIn': 'FI',
        'Random': 'RD',
        'Cinema': 'CM',
        'Target': 'TP',
        'Key9': 'K9',
        'KeyCoop': 'KC',
        'Key1': 'K1',
        'Key3': 'K3',
        'Key2': 'K2',
        'ScoreV2': 'SV',
        'Mirror': 'MR'
    }
    
    replay_mods_string = ""
    for mod in mods:
        if mod is "DoubleTime" or mod is "NightCore" or mod is "HardRock":
            continue
        replay_mods_string += mods_simplified[mod]

    if "NightCore" in mods:
        replay_mods_string += "NC"
    elif "DoubleTime" in mods:
        replay_mods_string += "DT"
    
    if "HardRock" in mods:
        replay_mods_string += "HR"

    if len(replay_mods_string) > 0:
        replay_mods_string = f"+{replay_mods_string}"
    
    return replay_mods_string

def calculate_grade(replay_data: Replay):
    # Total number of hits
    total_hits = replay_data.count_300 + replay_data.count_100 + replay_data.count_50 + replay_data.count_miss
    if total_hits == 0:
        return "Invalid input. Total hits must be greater than 0.", None

    # Calculate accuracy as a percentage
    accuracy = (300 * replay_data.count_300 + 100 * replay_data.count_100 + 50 * replay_data.count_50) / (300 * total_hits) * 100

    # Calculate proportions
    proportion_50 = replay_data.count_50 / total_hits

    # Determine the grade
    if accuracy == 100 and replay_data.count_miss == 0 and replay_data.count_50 == 0:
        grade = "SS"
    elif accuracy >= 95 and replay_data.count_miss == 0 and proportion_50 <= 0.01:  # Less than or equal to 1% 50s
        grade = "S"
    elif accuracy >= 90 and proportion_50 <= 0.05:  # Less than or equal to 5% 50s
        grade = "A"
    elif accuracy >= 80:
        grade = "B"
    elif accuracy >= 70:
        grade = "C"
    else:
        grade = "D"

    return grade

def get_desc(replay_data: Replay, sheet_data: ColumnSheetObr):
    if sheet_data["sliderbreaks"] and sheet_data["sliderbreaks"] > 0:
        return f"{sheet_data["sliderbreaks"]}sb"
    elif replay_data.count_miss > 0:
        return f"{replay_data.count_miss}❌"
    else:
        return ""
    