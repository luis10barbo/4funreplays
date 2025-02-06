
import os
import rosu_pp_py
from description.description_obr import save_description_obr
from model.config import get_config
from osu.local.folder import get_beatmap_file_path_by_hash, read_osu_db
from premiere.premiere import default_edit
from thumb.thumb import save_thumbnail_obr
from utils.osu import calculate_acc
from utils.replays_getter import get_replays_local_folder
from danser.danser_functions import record
from utils.google_sheets import parse_sheets_obr
from utils.logger import error,debug, info,setup_logger
from osu.web.osu_web import download_beatmap
from utils.arguments_parser import parse_arguments
from osrparse import Replay
from typing import cast

from utils.webdriver import create_browser

def main():
    config = get_config()
    program_args = parse_arguments()
    
    setup_logger()
    osu_db = read_osu_db()
    
    sheet = parse_sheets_obr()
    if not sheet:
        error("No sheet found")
        return
    
    replays = get_replays_local_folder()
    browser = create_browser()
    for replay in replays:
        replay_number = int(replay.rsplit("\\", 1)[1].replace(".osr", ""))

        # if replay_number != 8:
        #     continue

        print(len(sheet), replay_number)
        column = sheet[replay_number]
        if column["posted"] or column["approved"] is False or column["done"]:
            continue
        
        if program_args.record:
            record(config, replay, str(replay_number), column["skin_local"])

        with open(replay, "rb") as file:
        
            parsed_replay = cast(Replay, Replay.from_file(file)) # type: ignore

            beatmap_file = get_beatmap_file_path_by_hash(osu_db, parsed_replay.beatmap_hash)
            debug(f"Beatmap file {beatmap_file}")
            rosu_map = rosu_pp_py.Beatmap(path = beatmap_file)
            performance = rosu_pp_py.Performance(mods = parsed_replay.mods, 
                                                n300 = parsed_replay.count_300, n100 = parsed_replay.count_100, n50 = parsed_replay.count_50, n_geki = parsed_replay.count_geki, n_katu = parsed_replay.count_katu,
                                                accuracy = calculate_acc(parsed_replay),
                                                lazer = False,
                                                combo = parsed_replay.max_combo, misses = parsed_replay.count_miss, hitresult_priority = rosu_pp_py.HitResultPriority.BestCase)
            pp_data = performance.calculate(rosu_map)
            
            map_data = osu_db.beatmaps[parsed_replay.beatmap_hash]
            video_title =  f"{replay_number} - {parsed_replay.username} {map_data.song_title}".replace("\"", "").replace("'", "").replace("/", "").replace("?", "_").replace(":", "").replace(".", "")
            video_title_with_actual_nickname = None
            if program_args.description:
                video_title_with_actual_nickname = save_description_obr(browser, column, parsed_replay, pp_data, osu_db.beatmaps[parsed_replay.beatmap_hash], replay_number, True)

            if program_args.thumbnail:
                save_thumbnail_obr(browser, column, parsed_replay, pp_data, osu_db.beatmaps[parsed_replay.beatmap_hash], replay_number, video_title_with_actual_nickname if video_title_with_actual_nickname else video_title)

            if program_args.premiere:
                default_edit(os.path.join(config["danser_path"], "videos", f"{replay_number}.mp4"), video_title)
            
    info("Finished replay recording and thumbnail saving")
    browser.quit()
            

    arguments = parse_arguments()
    
    for column in sheet:
        if column["done"] == True or column["posted"] is True:
            continue
        
        if arguments.dl_maps is True: 
            download_beatmap(column["mapa"], file_name = f"{column["mapa"].rsplit('/', 1)[1]}.osz")


if __name__ == "__main__":
    main()