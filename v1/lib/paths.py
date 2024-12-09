import os

MAIN_DIRECTORY = os.getcwd()

# INFO DIRECTORY
INFO_PATH = os.path.join(MAIN_DIRECTORY, "info")

CONFIG_PATH = os.path.join(INFO_PATH, "config.json")
OUTPUT_DIRECTORY = os.path.join(INFO_PATH, "output")
SKINS_FILE = os.path.join(INFO_PATH, "skins.json")
REQUEST_FOLDER = os.path.join(INFO_PATH, "requests")
QUEUE_OUTPUT = os.path.join(INFO_PATH, 'queue.json')
QUEUE_VERSUS_OUTPUT = os.path.join(INFO_PATH, "versus", "queue.json")
PLAYER_CONFIGS = os.path.join(INFO_PATH, "playerconfigs.json")

# DOWNLOADS DIRECTORY
DOWNLOADS_PATH = os.path.join(MAIN_DIRECTORY, "downloads")

AVATAR_DOWNLOAD_PATH = os.path.join(DOWNLOADS_PATH, "avatars")
BEATMAPS_DOWNLOAD_PATH = os.path.join(DOWNLOADS_PATH, "beatmaps")
REPLAYS_DOWNLOAD_PATH = os.path.join(DOWNLOADS_PATH, "replays")

# SECRETS DIRECTORY
SECRETS_PATH = os.path.join(MAIN_DIRECTORY, "secrets")

OSU_SECRETS_PATH = os.path.join(SECRETS_PATH, "osu")
API_PATH = os.path.join(OSU_SECRETS_PATH, "api.txt")

# 4fun path
FUN_PATH = os.path.join(MAIN_DIRECTORY, "4fun")

PHOTOSHOP_TEMPLATES_PATH = os.path.join(FUN_PATH, "photoshop")
PREMIERE_TEMPLATES_PATH = os.path.join(FUN_PATH, "premiere")
