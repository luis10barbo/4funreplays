import os
import sys


PATH_ROOT = str(os.path.dirname(sys.modules['__main__'].__file__)) # type: ignore

PATH_CONFIG_FILE = os.path.join(PATH_ROOT, "config.json") 
PATH_REPLAYS_DIR = os.path.join(PATH_ROOT, "replays")
PATH_SHEET = os.path.join(PATH_ROOT, "sheet.txt")