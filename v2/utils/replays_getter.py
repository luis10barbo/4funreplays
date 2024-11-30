import os
from constants.paths import PATH_REPLAYS_DIR
from utils.logger import debug
def get_replays_local_folder():
    debug(f"Getting replays from folder {PATH_REPLAYS_DIR}")
    replays = os.listdir(PATH_REPLAYS_DIR)
    replays_abs = [os.path.join(PATH_REPLAYS_DIR, replay) for replay in replays]

    debug(f"Found {len(replays)} replays")
    return replays_abs