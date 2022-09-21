from calendar import c
from lib import logger, time, osu
from lib.paths import OUTPUT_DIRECTORY


import os
import time
import subprocess

import pymiere
from pymiere.wrappers import time_from_seconds

premiere_path = r"C:\Program Files\Adobe\Adobe Premiere Pro 2021\Adobe Premiere Pro.exe"
premiere_executable = "Adobe Premiere Pro.exe"
MAIN_DIRECTORY = os.getcwd()

def check_if_premiere_alive(TIMEOUT=2, open_premiere=False, retry=True):
    is_first_check = True
    while 1:
        try:
            pymiere.objects.app
            logger.info("Adobe Premiere Pro is open")
            return True
        except:
            if is_first_check == True:
                # First check message
                if open_premiere == True:
                    premiere_process = subprocess.Popen(f'"{premiere_path}"')
                    logger.info("Opening Adobe Premiere Pro")
                else:
                    logger.error("Adobe Premiere Pro isn't open, pausing program till you open it", notify=True)
        is_first_check = False
            
        if retry == False:
            # If not retry, stop
                return False
        time.sleep(TIMEOUT)

def kill_premiere():
    os.system(f'taskkill /F /IM "Adobe Premiere Pro.exe"')

def middle_two_captions(upper_text, lower_text):
    app = pymiere.objects.app
    project = app.project
    caption_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "captions", "Untitled.mogrt")
    
    # Add caption
    caption_video_track = 1
    caption = project.activeSequence.importMGT(caption_path, 0, caption_video_track, 0)
    
    components : pymiere.Component = caption.components
    for component in components:
        component : pymiere.Component
        print(f"component > {component.displayName}")
        for prop in component.properties:
            prop : pymiere.Properties
            if prop.displayName == "Upper":
                prop.setValue(upper_text, True)
                
            if prop.displayName == "Lower":
                prop.setValue(lower_text, True)

def validate_video(video_path:str) -> bool:
    if not os.path.isfile(video_path):
        logger.error(f"{video_path} is not a file!")
        return 1
    
    file_extension = video_path.rsplit(".", 1)[1]
    
    if file_extension != "mp4":
        logger.error("Only mp4 files are supported!")
        return 1

    return 0

def versus_edit(video_path_1, video_path_2, output_name):
    project_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "projects", "neu.prproj")
    endscreen_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "captions", "endscreen.mogrt")
    # rootItem changeMediaPath
    
    check_if_premiere_alive(open_premiere=True)
    
    app = pymiere.objects.app
    project = app.project
    sequence = project.activeSequence
    
    map_name = "boga"
    difficulty_name = "[waggers]"
    n300x = "3005"
    n100x = "32"
    n50x = "2"
    n0x = "30"
    grade = "A"
    accuracy = "90.64%"
    pp = "300pp"
    
    # project.closeDocument(False)
    app.openDocument(project_path)
    
    plays_track = sequence.videoTracks[0]
    overlay_track = sequence.videoTracks[1]
    
    # End Screen
    # Import background Path
    play_end_time = plays_track.clips[-1].end.seconds
    
    background_path = r"D:\osu2\Songs\1340038 ZAQ - Caste Room\asdf.jpg"
    project.importFiles([background_path], True, project.getInsertionBin(), False)
    background_bin_item = project.rootItem.findItemsMatchingMediaPath(background_path, ignoreSubclips=False)
    
    # plays_track.insertClip(background_bin_item[0], play_end_time) # insert bg at track
    # background_clip = plays_track.clips[-1] # get latest media from track (bg)
    # background_clip.end = time_from_seconds(background_clip.start.seconds + 5) # set duration to 10s
    
    endscreen = sequence.importMGT(endscreen_path, play_end_time - 5, 1, 0)
    endscreen.end = time_from_seconds(endscreen.start.seconds + 10)
    components : pymiere.Component = endscreen.components
    for component in components:
        component : pymiere.Component
        # if component.displayName == "Opacidade":
        #     for prop in component.properties:
        #         prop : pymiere.Properties
        #         a = prop.displayName
        #         print(a, "waga")
        # print(f"component > {component.displayName}")
        for prop in component.properties:
            prop : pymiere.Properties
            if prop.displayName == "map":
                prop.setValue(map_name, True)
                
            elif prop.displayName == "difficulty":
                prop.setValue(difficulty_name, True)

            elif prop.displayName == "x300":
                prop.setValue(n300x, True)
                
            elif prop.displayName == "x100":
                prop.setValue(n100x, True)
                
            elif prop.displayName == "x50":
                prop.setValue(n50x, True)
                
            elif prop.displayName == "x0":
                prop.setValue(n0x, True)

            elif prop.displayName == "grade":
                prop.setValue(grade, True)

            elif prop.displayName == "accuracy":
                prop.setValue(accuracy, True)
                
            elif prop.displayName == "pp":
                prop.setValue(pp, True)
            
    # end_time = time.time_from_seconds(play_end_time + 1)
    # print(end_time.minute, end_time.second)


def funreplays_edit(video_path:str, output_name:str, map_name:str, difficulty_name:str, n300x:int, n100x:int, n50x:int, n0x:int, grade:str, accuracy:str, pp:str, combo:int):
    project_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "projects", "4fun.prproj")
    render_preset_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "presets", "good quality mb.epr")
    endscreen_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "captions", "endscreen.mogrt")
    
    if validate_video(video_path) == 1:
        logger.error("Error on validation, video editing stopped.")
        return 
    
    # Check if premiere is open
    check_if_premiere_alive(open_premiere=True)

    app = pymiere.objects.app
    project = app.project
    
    # Close document if one is open
    if app.isDocumentOpen() and project.name.split(".",1)[0] == "4fun":
        project.closeDocument(False)
        logger.info("Current project closed without saving.")
        
    app.openDocument(project_path)
    
    logger.info(f"Opening video {video_path}")
    project.importFiles([video_path], True, project.getInsertionBin(), False)
    bin_video = project.rootItem.findItemsMatchingMediaPath(video_path, ignoreSubclips=False)
    video_sequence = project.activeSequence
    
    # Add clip to sequence
    plays_track = video_sequence.videoTracks[0]
    plays_track.insertClip(bin_video[0], time_from_seconds(6))
    
    play_end_time = plays_track.clips[-1].end.seconds
    
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
    endscreen = video_sequence.importMGT(endscreen_path, play_end_time - 2.5, 1, 0)
    endscreen.end = time_from_seconds(endscreen.start.seconds + 10)
    components : pymiere.Component = endscreen.components
    for component in components:
        component : pymiere.Component
        # if component.displayName == "Opacidade":
        #     for prop in component.properties:
        #         prop : pymiere.Properties
        #         a = prop.displayName
        #         print(a, "waga")
        # print(f"component > {component.displayName}")
        for prop in component.properties:
            prop : pymiere.Properties
            match(prop.displayName):
                
                case "map":
                    prop.setValue(map_name, True)
                    
                case "difficulty":
                    prop.setValue(f"[{difficulty_name}]", True)

                case "x100":
                    prop.setValue(f"{n100x}", True)
                    
                case "x50":
                    prop.setValue(f"{n50x}", True)
                    
                case "x0":
                    prop.setValue(f"{n0x}", True)

                case "grade":
                    prop.setValue(grade, True)

                case "accuracy":
                    prop.setValue(f"{accuracy}%", True)
                    
                case "pp":
                    prop.setValue(f"{pp}pp", True)
                    
                case "combo":
                    prop.setValue(f"{combo}x combo", True)
    
    output_path = os.path.join(OUTPUT_DIRECTORY, f"{output_name}.mp4")
    
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