import os
import sys


PATH_ROOT = str(os.path.dirname(sys.modules['__main__'].__file__)) # type: ignore

PATH_CONFIG_FILE = os.path.join(PATH_ROOT, "config.json") 
PATH_REPLAYS_DIR = os.path.join(PATH_ROOT, "replays")
PATH_SHEET = os.path.join(PATH_ROOT, "sheet.txt")
PATH_OSU_SESSION = os.path.join(PATH_ROOT, "secrets", "osu_session")
PATH_OSU_BEATMAPS_DOWNLOADS = os.path.join(PATH_ROOT, "downloads", "beatmaps")

PATH_THUMB_FOLDER = os.path.join(PATH_ROOT, "thumb")
PATH_OBR_THUMB_FILE = os.path.join(PATH_THUMB_FOLDER, "obrThumb.html")
PATH_THUMB_FOLDER_FILES = os.path.join(PATH_THUMB_FOLDER, "files")

PATH_DESCRIPTION_FOLDER = os.path.join(PATH_ROOT, "description")
PATH_DESCRIPTION_FOLDER_FILES = os.path.join(PATH_DESCRIPTION_FOLDER, "files")

PATH_PREMIERE_FOLDER = os.path.join(PATH_ROOT, "premiere")
PATH_PREMIERE_FOLDER_OUT = os.path.join(PATH_PREMIERE_FOLDER, "out")
PATH_PREMIERE_FOLDER_PROJECTS = os.path.join(PATH_PREMIERE_FOLDER, "projects")
PATH_PREMIERE_FOLDER_PRESETS = os.path.join(PATH_PREMIERE_FOLDER, "presets")
