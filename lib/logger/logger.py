import win10toast
from lib import time
import logging
import os

LOGS_FOLDER = os.path.join(os.getcwd(), "info", "logs")
log_file = f"{os.path.join(LOGS_FOLDER, f'{time.get_current_time_computer(spaces=True)}.log')}"
TITLE = "4funreplays"

logging.basicConfig(
    filename=f"{log_file}",
    encoding="utf-8",
    level=logging.DEBUG,
    format= "| {asctime} | {levelname:<8} > {message}",
    style="{",
    filemode="w"
)

def debug(message:str=""):
    PREFIX = "DEBUG: "
    logging.debug(f"{PREFIX}{message}")

def info(message:str="", notify:bool=False):
    PREFIX = f"INFO: "
    print(f"{PREFIX}{message}")
    logging.debug(f"{PREFIX}{message}")
    
    if notify == True:
        win10toast.ToastNotifier().show_toast(TITLE, msg=f"{PREFIX}{message}")

def warn(message:str=""):
    PREFIX = "WARNING: "
    logging.warning(f"{PREFIX}{message}")

def error(message:str="", notify:bool=False):
    PREFIX = "ERROR: "
    print(f"{PREFIX}{message}")
    logging.error(f"{PREFIX}{message}")
    
    if notify == True:
        win10toast.ToastNotifier().show_toast(TITLE, msg=f"{PREFIX}{message}")

def fatal(message:str=""):
    PREFIX = "FATAL: "
    print(f"{PREFIX}{message}")
    logging.error(f"{PREFIX}{message}")
    exit()
    
