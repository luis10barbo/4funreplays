import gdown
from lib import logger
import os

def download_from_drive(url:str, download_directory:str, file_name:str):
    if url == "":
        logger.error("No link has been specified!")
        return
    
    if not os.path.isdir(download_directory):
        logger.error("Specified directory is invalid.")
        return

    if file_name == "":
        logger.error("No file name has been specified!")
        return
    
    output_path = f"{os.path.join(download_directory, file_name)}"

    logger.info(f"Downloading file from {url} to {output_path}")
     
    # Download
    gdown.download(url, output_path, quiet=False, fuzzy=True)
    
    # Remove temporary files
    temporary_files = [os.path.join(download_directory, file) for file in os.listdir(download_directory) if file.endswith(".tmp")]
    
    for file_path in temporary_files:
        try:
            os.remove(file_path)
        except:
            logger.error(f"Temporary file '{file_path}' wasn't able to be removed.")
            
    return output_path