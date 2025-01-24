import os
from tkinter import Tk, filedialog
from constants.paths import PATH_REPLAYS_DIR
from model.config import get_config
from utils.logger import debug
def get_replays_local_folder():
    debug(f"Getting replays from folder {PATH_REPLAYS_DIR}")
    replays = os.listdir(PATH_REPLAYS_DIR)
    replays_abs = [os.path.join(PATH_REPLAYS_DIR, replay) for replay in replays]

    debug(f"Found {len(replays)} replays")
    return replays_abs

def select_replay():
    config = get_config()
    root = Tk()
    root.withdraw()
    replay_dir = filedialog.askopenfilename(title="Select replay", initialdir=f"{os.path.join(config['osu_path'], "Replays")}", filetypes=[("Arquivos de replay", "*.osr")])

    return [replay_dir]