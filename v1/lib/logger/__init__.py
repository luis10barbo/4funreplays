import os
from lib import time

def clean_log_folder():
    # YOU DON'T HAVE ANY IDEA HOW MUCH TIME I'VE PASSED TRYING TO WRITE THIS F****NG PEACE OF SHIT CODEEEEEEEEEEEE
    """
    Checks if files in logs folder surpass the limit
    """
    LOGS_FOLDER = os.path.join(os.getcwd(), "info", "logs")
    log_limit = 5
    
    
    log_files = os.listdir(LOGS_FOLDER)
    
    target_deletion_number = - len(log_files) + (log_limit - 1)
    
    # Sort log dates
    date_list:list[time.datetime] = []
    for current_file in log_files:
        file_date = time.time_from_string(current_file.rsplit(".", 1)[0])
        date_list.append(file_date)
        
    # Reverse sort list
    former_to_recent_list = sorted(date_list)
    
    # Remove extra logs
    while not target_deletion_number >= 0:
        # Has less than log_limit files in logs folder
        os.remove(f"{os.path.join(LOGS_FOLDER, time.string_from_time(former_to_recent_list[0]))}.log")
        del former_to_recent_list[0]
        
        target_deletion_number += 1
            

clean_log_folder()

from .logger import debug, error, fatal, info, warn

