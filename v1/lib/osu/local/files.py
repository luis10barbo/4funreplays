import os
import subprocess
import time
from lib import logger


def remove_illegal_characters(string: str):
    string = string.replace(":", "")
    return string


class OsuFolderHandler:
    osu_path = ""

    def __init__(self, config: dict) -> None:
        self.load_path_from_config(config)

    def load_path_from_config(self, config: dict):
        self.osu_path = config["Directories"]["Osu!"]

    def get_beatmapset_path_by_string(self, target_string: str) -> str:
        """
        Search for songs that contain 'target_string' at Songs folder
        """
        logger.info(
            f"Getting beatmapset that matches string '{target_string}'")

        songs_path = os.path.join(self.osu_path, "Songs")
        folder_content = os.listdir(songs_path)

        # Create list from strings that contain 'song_id' at songs folder
        matching_beatmapsets = [os.path.join(
            songs_path, beatmapset) for beatmapset in folder_content if target_string.lower() in beatmapset.lower()]

        return logger.error(f"No beatmapset found that matches {target_string}") if matching_beatmapsets == [] else matching_beatmapsets[0]

    def check_if_skin_exists(self, target_skin: str) -> bool:
        """
        Check if skin 'target_skin' exists at Skins folder.
        """

        logger.info(f"Checking if '{target_skin} exists at osu! folder!'")

        skins_path = os.path.join(self.osu_path, "Skins")

        folder_content = os.listdir(skins_path)

        if target_skin not in folder_content:
            logger.info("Skin doesn't exist.")
            return False
        logger.info("Skin exists!")
        return True

    def get_background_path_from_difficulty(self, beatmapset_path: str, target_difficulty: str) -> str:
        """
        Gets beatmap background of difficulty 'target_dificulty'(without '[]') from beatmapset 'beatmapset_path'
        """
        logger.info(
            f"Getting background from difficulty '{target_difficulty}' from beatmapset '{beatmapset_path}'")

        beatmapset_content = os.listdir(beatmapset_path)
        if beatmapset_content == []:
            return None

        difficulty_path = self.get_beatmapset_difficulty_by_string(
            beatmapset_path, target_difficulty)

        with open(difficulty_path, "r", encoding="utf-8") as file:
            difficulty_file = file.read()

        # Try parsing event section
        try:
            events_section: str = difficulty_file.split("[Events]")[
                1].split("\n")
            for line in events_section:
                if not line.startswith("0,0,"):
                    continue
                background = events_section[2].split(",")[2]
                if background.startswith("\"") and background.endswith("\""):
                    background = background[1:][:-1]
                else:
                    raise Exception()
        except:
            logger.info("No background found")
            return None
        background_path = os.path.join(beatmapset_path, background)

        return background_path

    def get_beatmapset_difficulty_by_string(self, beatmapset_path: str, target_difficulty: str) -> str:
        logger.info(
            f"Getting matching difficulty '{target_difficulty}' from beatmapset '{beatmapset_path}'")
        target_difficulty = remove_illegal_characters(target_difficulty)
        matching_files = [os.path.join(beatmapset_path, file) for file in os.listdir(
            beatmapset_path) if "[" + target_difficulty.lower() + "]" in file.lower()]

        return logger.error(f"No beatmap difficulty found that matches {target_difficulty}") if matching_files == [] else matching_files[0]

    def open_beatmap(self, beatmap_path):
        osu = os.path.join(self.osu_path, "osu!.exe")

        logger.info(f"Opening beatmap {beatmap_path} with osu {osu}")
        subprocess.Popen([f"{osu}", f"{beatmap_path}"])

        time.sleep(15)
        os.system("taskkill /F /IM osu!.exe")

    def validate_skin(self, skin_name: str, skin_link: str = ""):
        # TODO: Create automated skin download
        if skin_name == "Skin Privada ( me mande no privado luis10barbo#3251 )":
            return

        logger.debug(f"Validating skin {skin_name}")
        skins_path = os.path.join(self.osu_path, "Skins")
        while 1:
            if not skin_name in os.listdir(skins_path):
                logger.error(
                    f"Skin {skin_name} not found at osu! skins directory, download it and try again", True)
                logger.info(
                    f"You can download it at {f'{skin_link}' if skin_link != '' else 'No link provided'}")
                input("Press enter after downloading")
                continue
            break

        logger.debug(f"Skin {skin_name} exists at osu! folder")
