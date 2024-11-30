
from model.config import get_config, Config
from utils.replays_getter import get_replays_local_folder
from danser.danser_functions import record
from utils.google_sheets import parse_sheets_obr
from utils.logger import error
from osu.web.osu_web import download_beatmap
from utils.arguments_parser import parse_arguments
def main():
    config: Config | None = get_config()
    if config is None:
        error("No config found")
        return
    
    sheet = parse_sheets_obr()
    if not sheet:
        error("No sheet found")
        return
    
    replays = get_replays_local_folder()
    for replay in replays:
        replay_number = int(replay.rsplit("\\", 1)[1].replace(".osr", ""))
        column = sheet[replay_number]
        if column["done"] is True or column["posted"] is True:
            continue

        record(config, replay, str(replay_number), column["skin_local"])

    arguments = parse_arguments()
     
    for column in sheet:
        if column["done"] == True or column["posted"] is True:
            continue
        
        if arguments.dl_maps is True: 
            download_beatmap(column["mapa"], file_name = f"{column["mapa"].rsplit('/', 1)[1]}.osz")

if __name__ == "__main__":
    main()