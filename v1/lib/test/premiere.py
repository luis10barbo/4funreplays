import os
import pymiere
from pymiere.wrappers import time_from_seconds
import time

import subprocess

import lib
from lib import logger

premiere_path = r"C:\Program Files\Adobe\Adobe Premiere Pro 2021\Adobe Premiere Pro.exe"
MAIN_DIRECTORY = os.getcwd()

class PremiereHandler():    
    def check_if_premiere_open(self, retry=True, TIMEOUT=5):
        while 1:
            try:
                pymiere.objects.app
                logger.info("Premiere is open!")
                return True
            except:
                logger.error("Premiere isn't open!")
                self.premiere_process = subprocess.Popen(f'"{premiere_path}"')
            if retry == False:
                return False
            time.sleep(TIMEOUT)

    def kill_premiere():
        os.system('taskkill /F /IM "Adobe Premiere Pro.exe"')

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

    def validate_video(self, video_path:str) -> bool:
        if not os.path.isfile(video_path):
            logger.error(f"{video_path} is not a file!")
            return 1
        
        file_extension = video_path.rsplit(".", 1)[1]
        
        if file_extension != "mp4":
            logger.error("Only mp4 files are supported!")
            return 1

        return 0
    
    def funreplays_edit(self, video_path=""):
        project_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "projects", "4fun.prproj")
        
        if self.validate_video(video_path) == 1:
            logger.error("Error on validation, video editing stopped.")
            return 
        
        # Check if premiere is open
        if self.check_if_premiere_open() == False:
            return
    
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
        

        # Add clip to sequence
        videos_sequence = project.activeSequence.videoTracks[0]
        videos_sequence.insertClip(bin_video[0], time_from_seconds(6))
        
        # Preparation for future end-screen
        # video_end_time = videos_sequence.clips[-1].end.seconds
        # end_time = lib.time.time_from_seconds(video_end_time)
        # print(end_time.minute, end_time.second)

    
    def test_edit(self):
        videos_path = r"G:\videos\danser\videos"
        
        project_path = os.path.join(MAIN_DIRECTORY, "lib", "premiere", "projects", "test.prproj")
        
        app = pymiere.objects.app
        project = app.project

        # Close document if one is open
        if app.isDocumentOpen():
            project.closeDocument(False)
            logger.info("Current project closed without saving, sorry.")

        # Open project
        app.openDocument(project_path)
        
        
        # Import clips
        logger.info("Opening clips")
        clips = [r"G:\videos\danser\videos\1.mp4"]
        project.importFiles(clips, True, project.getInsertionBin(), False)
        bin_item = project.rootItem.findItemsMatchingMediaPath(clips[0], ignoreSubclips=False)
        
        # Create Sequence
        project.createNewSequenceFromClips("Python Sequence", bin_item)
        
        project.activeSequence.videoTracks[0].insertClip()
    
        
        # self.kill_premiere()
        