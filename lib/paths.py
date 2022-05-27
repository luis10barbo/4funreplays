import os

MAIN_DIRECTORY = os.getcwd()

# INFO DIRECTORY 
INFO_PATH = os.path.join(MAIN_DIRECTORY, "info")

CONFIG_PATH = os.path.join(INFO_PATH, "config.json")
OUTPUT_DIRECTORY = os.path.join(INFO_PATH, "output")
SKINS_FILE = os.path.join(os.getcwd(), "info", "skins.json")

# SECRETS DIRECTORY 
SECRETS_PATH = os.path.join(MAIN_DIRECTORY, "secrets")

OSU_SECRETS_PATH = os.path.join(SECRETS_PATH, "osu")
API_PATH = os.path.join(OSU_SECRETS_PATH, "api.txt")