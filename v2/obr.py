
from model.config import get_config, Config
from utils.replays_getter import get_replays_local_folder
from danser.danser_functions import record
from utils.google_sheets import parse_sheets_obr
from utils.logger import error
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
    for i, replay in enumerate(replays):
        record(config, replay, str(i))

if __name__ == "__main__":
    main()