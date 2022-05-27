import traceback
from osrparse import Replay

from lib import logger

from .gosu_pp import gosu_python

def calculate_accuracy() -> float:
    pass

def calculate_pp(difficulty_path:str, replay_info:Replay) -> float:
    mods = f"{f'{replay_info.mod_combination}'.replace('Mod.', '')}"

    
    logger.debug(f"Calculating pp for {difficulty_path}, with mods {mods}")
    try:
        pp, error = gosu_python.get_pp(osu_path=difficulty_path, mods=mods, max_combo=f"{replay_info.max_combo}", n300s=f"{replay_info.number_300s}", n100s=f"{replay_info.number_100s}", n50s=f"{replay_info.number_50s}", nmisses=f"{replay_info.misses}")
        if error != None:
            logger.error(error)
            raise Exception
    except:
        traceback.print_exc()
        pp = float(input("Write a the pp value here: "))

    return pp
def calculate_star_rating(difficulty_path:str, replay_info:Replay) -> float:
    mods = f"{f'{replay_info.mod_combination}'.replace('Mod.', '')}"
    
    logger.debug(f"Calculating star rating for {difficulty_path}, with mods {mods}")
    try:
        star_rating, error = gosu_python.get_star_rating(osu_path=difficulty_path, mods=mods)
        if error != None:
            logger.error(error)
            raise Exception
    except:
        traceback.print_exc()
        star_rating = float(input("Write a Star Rating Here: "))
    return star_rating

def is_replay_at_leaderboard(replay_info:Replay, top_beatmap_scores:list) -> int:
    """For each score in top_beatmap_scores, check if it's equal to replay_info"""
    for score, i in zip(top_beatmap_scores, range(len(top_beatmap_scores))):
        current_position = i + 1
        local_replay = {
            "misses" : f"{replay_info.misses}",
            "50" : f"{replay_info.number_50s}",
            "100" : f"{replay_info.number_100s}",
            "300" : f"{replay_info.number_300s}",
            "countkatu" : f"{replay_info.katus}",
            "countgeki" : f"{replay_info.gekis}",
            "is_perfect" : f"{1 if replay_info.is_perfect_combo == True else 0}"
        }
        
        web_score = {
            "misses" : score["countmiss"],
            "50" : score["count50"],
            "100" : score["count100"],
            "300" : score["count300"],
            "countkatu" : score["countkatu"],
            "countgeki" : score["countgeki"],
            "is_perfect" : score["perfect"]
        }
        if local_replay == web_score:
            logger.info(f"Replay is at position {current_position}")
            return current_position
        
    return 0
    
    logger.info("Replay is not at scores")