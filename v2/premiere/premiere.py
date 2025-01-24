import os
import subprocess
import time

import pymiere
from pymiere.wrappers import time_from_seconds # type: ignore
from constants.paths import PATH_PREMIERE_FOLDER_OUT, PATH_PREMIERE_FOLDER_PRESETS, PATH_PREMIERE_FOLDER_PROJECTS
from model.config import get_config
from utils import logger
def check_if_premiere_alive(timeout:int = 2, open_premiere:bool = False, retry:bool = True):
    config = get_config()
    is_first_check = True
    while True:
        try:
            pymiere.objects.app
            logger.info("Adobe Premiere Pro is open")
            return True
        except:
            if is_first_check == True:
                # First check message
                if open_premiere == True:
                    subprocess.Popen(f'"{config["premiere_path"]}"')
                    logger.info("Opening Adobe Premiere Pro")
                else:
                    logger.error("Adobe Premiere Pro isn't open, pausing program till you open it")
        is_first_check = False
            
        if retry == False:
            # If not retry, stop
                return False
        time.sleep(timeout)

def kill_premiere():
    os.system(f'taskkill /F /IM "Adobe Premiere Pro.exe"')

def validate_video(video_path:str) -> bool:
    if not os.path.isfile(video_path):
        logger.error(f"{video_path} is not a file!")
        return False
    
    file_extension = video_path.rsplit(".", 1)[1]
    
    if file_extension != "mp4":
        logger.error("Only mp4 files are supported!")
        return False

    return True


def default_edit(video_path:str, output_name:str):
    project_path = os.path.join(PATH_PREMIERE_FOLDER_PROJECTS, "obr.prproj")
    render_preset_path = os.path.join(PATH_PREMIERE_FOLDER_PRESETS, "240.epr")
    
    if not validate_video(video_path):
        logger.error("Error on validation, video editing stopped.")
        return 
    
    # Check if premiere is open
    check_if_premiere_alive(open_premiere=True)

    app = pymiere.objects.app
    project = app.project 
    
    # Close document if one is open
    if app.isDocumentOpen():
        project.closeDocument(False)
        logger.info("Current project closed without saving.")
    
    app.openDocument(project_path)
    video_sequence = project.activeSequence
    
    logger.info(f"Opening video {video_path}")
    project.importFiles(  
        [video_path], # can import a list of media  
        suppressUI=True,  
        targetBin=project.getInsertionBin(),  
        importAsNumberedStills=False  
    )  
    print(video_path)
    # find media we imported  
    items = project.rootItem.findItemsMatchingMediaPath(video_path.replace("/", "\\"), ignoreSubclips=False)  
    # add clip to active sequence
    for item in items:
        print(item)
    project.activeSequence.videoTracks[0].insertClip(items[0], time_from_seconds(0))
    
    # play_end_time = plays_track.clips[-1].end.seconds
    
    # Preparation for future end-screen
    # video_end_time = videos_sequence.clips[-1].end.seconds
    # end_time = lib.time.time_from_seconds(video_end_time)
    # print(end_time.minute, end_time.second)
    
    # map_name = "boga"
    # difficulty_name = "[waggers]"
    # n300x = "3005"
    # n100x = "32"
    # n50x = "2"
    # n0x = "30"
    # grade = "A"
    # accuracy = "90.64%"
    # pp = "300pp"

    logger.info("Adding endscreen")
    # endscreen = video_sequence.importMGT(endscreen_path, play_end_time - 2.5, 1, 0)
    # endscreen.end = time_from_seconds(endscreen.start.seconds + 10)
    # components = cast(list[pymiere.Component], endscreen.components) # type: ignore
    # for component in components:
    #     component : pymiere.Component
    #     # if component.displayName == "Opacidade":
    #     #     for prop in component.properties:
    #     #         prop : pymiere.Properties
    #     #         a = prop.displayName
    #     #         print(a, "waga")
    #     # print(f"component > {component.displayName}")
    #     for prop in cast(list[pymiere.Properties], component.properties): #type: ignore
    #         prop : pymiere.Properties
    #         match(prop.displayName):
                
    #             case "map":
    #                 prop.setValue(map_name, True)
                    
    #             case "difficulty":
    #                 prop.setValue(f"[{difficulty_name}]", True)

    #             case "x100":
    #                 prop.setValue(f"{n100x}", True)
                    
    #             case "x50":
    #                 prop.setValue(f"{n50x}", True)
                    
    #             case "x0":
    #                 prop.setValue(f"{n0x}", True)

    #             case "grade":
    #                 prop.setValue(grade, True)

    #             case "accuracy":
    #                 prop.setValue(f"{accuracy}%", True)
                    
    #             case "pp":
    #                 prop.setValue(f"{pp}pp", True)
                    
    #             case "combo":
    #                 prop.setValue(f"{combo}x combo", True)
    
    output_path = os.path.join(PATH_PREMIERE_FOLDER_OUT, f"{output_name}.mp4".replace("?", ""))
    
    try:
        logger.info("Rendering video")
        video_sequence.exportAsMediaDirect(
                    output_path,
                    render_preset_path,
                    pymiere.objects.app.encoder.ENCODE_ENTIRE
        )
    except:
        print("Unknown error has ocourred")
        check_if_premiere_alive()
    
    kill_premiere()   