import json
import os
from . import google
from .offline import offline

from lib import logger, discord, player

import lib

import requests

from lib.osu.web.session import OSU_BEATMAPS_DOWNLOAD_PATH
from lib.replays import REPLAYS_DIRECTORY


class QueueManager:
    queue: list[dict] = []
    queue_type = ""
    has_updated_spreadsheet = False

    def __init__(self, queue_type="4funreplays"):
        self.queue_type = queue_type

    def set_queue(self, queue: dict[str]):
        self.queue = queue
        print(queue)
        for queue_entry in queue:
            player.update_player_config(
                (queue_entry["profile"].replace("u/", "users/", ).rsplit("users/", 1)[1].split("/", 1)[0]), skin=queue_entry["skin"], cursor_size=queue_entry["cursor_size"])

    def verify_skins(self, osu_folder_handler, skin_handler):
        for queue_entry in self.queue:
            osu_folder_handler.validate_skin(
                queue_entry["skin"], skin_handler.get_skin_by_name(queue_entry["skin"])["link"])

    def type_chooser(self, config_json: dict[str, dict], predefined_answer: str = ""):
        types = ["google", "local"]

        target_type = predefined_answer

        if target_type not in types and target_type != "":
            lib.logger.error(f"Predefined type '{target_type}' not found!")
            target_type = ""

        if target_type == "":
            target_type = lib.prompt.from_list(
                "Choose from where you want to get your self.queue", types, predefined_answer)

        match(target_type):
            case "google":
                self.get_queue_from_google(config_json)
            case "local":
                self.get_queue_from_local_folder()

    def get_queue_from_google(self, config_json: dict[str, dict]):
        google_spreadsheet = google.GoogleSpreadsheetHandler()
        google_spreadsheet.get_spreadsheet_id_from_config(config_json)
        self.set_queue(google_spreadsheet.get_queue_from_google())

        self.has_updated_spreadsheet = True
        lib.funreplays.clear_folders()

    def get_queue_from_local_folder(self):
        lib.logger.info("Opening self.queue from local folder")

        if self.queue_type == "4funreplays":
            queue_output = lib.paths.QUEUE_OUTPUT

        elif self.queue_type == "versus":
            queue_output = lib.paths.QUEUE_VERSUS_OUTPUT

        if not os.path.isfile(queue_output):
            lib.logger.error(f"No self.queue file found at {queue_output}")
            return

        with open(queue_output, "r") as file:
            self.set_queue(json.load(file))

    def get_queue_from_tracker(self, timespan="week"):
        discord_bot = discord.DiscordBot()
        discord_bot.get_queue_from_tracker(timespan)

    def filter_queue(self, answer="", filter_answer=""):
        if answer == "":
            answer = lib.prompt.yes_or_no(
                "Do you wish to modify any entries from the self.queue")

        match(answer):
            case "y":
                answer = False
                while answer != True:
                    # Give input for self.queue answer if filter_answer isn't ""
                    if filter_answer == "":
                        answer = input("Type d for delete or k to keep as the first letter, then write a \"-\" and the self.queue numbers, separated by a comma, that you want to delete/keep \
                            \n(Example : \n\"d-1,2,4\" > deletes 1,2,4 from self.queue \n\"k-1,2,4\" > deletes everything but 1,2,4) : "
                                       )
                    else:
                        answer = filter_answer
                    first_character = answer[0]
                    if first_character == "k" or first_character == "d":
                        # Get numbers from string and transform them into integers
                        answer_numbers = [int(number)
                                          for number in answer[2:].split(",")]

                        match(first_character):
                            case "d":
                                # Loop to check which entries match to numbers
                                for entry_number in range(len(self.queue)):
                                    entry = self.queue[entry_number]

                                    # Turning matches into None, to delete in the future
                                    if entry["replay_id"] in answer_numbers:
                                        self.queue[entry_number] = None

                            case "k":

                                # Loop to check which entries match to numbers
                                for entry_number in range(len(self.queue)):
                                    entry = self.queue[entry_number]

                                    # Turning matches into None, to delete in the future
                                    if entry["replay_id"] not in answer_numbers:
                                        self.queue[entry_number] = None

                        # Create new list for elements that aren't None
                        new_list = []

                        for entry in self.queue:
                            if entry != None:
                                new_list.append(entry)

                        self.queue = new_list

                        # Reset self.queue_answer
                        filter_answer = ""

                        answer = True
                return
            case "n":
                return

    def should_download_replay(self, output_path: str) -> bool:
        if self.has_updated_spreadsheet == True:
            return True
        if os.path.isfile(output_path) == False:
            return True
        return False

    def get_replays_from_queue(self, force=False):
        if self.queue_type == "4funreplays":
            replay_types = ["4funreplays"]
        elif self.queue_type == "versus":
            replay_types = ["replay_1", "replay_2"]

        for queue_entry in self.queue:
            # TODO: remove repeated code here
            if self.queue_type == "4funreplays":
                # 4funreplays
                file_name = f"{queue_entry['replay_id']}.osr"
                replay_path = os.path.join(REPLAYS_DIRECTORY, file_name)

                if self.should_download_replay(replay_path):
                    file_url = f"{queue_entry['replay_link']}"

                    # Run conditions:
                    # - Force = True
                    # - has updated spreadsheet = true
                    # - has not updated spreadsheet but replay doesn't exist
                    queue_entry["replay"] = lib.replays.download_replay(
                        file_url, file_name)

                else:
                    queue_entry["replay"] = replay_path

            elif self.queue_type == "versus":
                for current_replay in replay_types:
                    # versus
                    file_name = f"{queue_entry[current_replay]['replay_id']}_{current_replay}.osr"
                    replay_path = os.path.join(REPLAYS_DIRECTORY, file_name)

                    logger.debug(f"replay path {replay_path}")

                    if self.should_download_replay(replay_path):
                        file_url = f"{queue_entry[current_replay]['replay_link']}"

                        # Run conditions:
                        # - Force = True
                        # - has updated spreadsheet = true
                        # - has not updated spreadsheet but replay doesn't exist
                        queue_entry[current_replay]["replay"] = lib.replays.download_replay(
                            file_url, file_name)

                    else:
                        queue_entry[current_replay]["replay"] = replay_path

    def download_beatmaps_from_queue(self, osu_session: lib.osu.web.OsuSessionHandler, osu_files: lib.osu.local.OsuFolderHandler, force=False):
        if not self.has_updated_spreadsheet and force == False:
            logger.info(
                "Spreadsheet hasn't been updated, ignoring download of beatmaps!")
            return

        for queue_entry in self.queue:
            beatmapset_url = f"{queue_entry['map'].split('#osu/')[0]}"
            file_name = f"{beatmapset_url.rsplit('/', 1)[1]}.osz"

            osu_session.download_beatmap(beatmapset_url, file_name)

        self.open_downloaded_beatmaps(osu_files)

    def open_downloaded_beatmaps(self, osu_files: lib.osu.local.OsuFolderHandler):
        beatmaps = [os.path.join(OSU_BEATMAPS_DOWNLOAD_PATH, file) for file in os.listdir(
            OSU_BEATMAPS_DOWNLOAD_PATH) if file.endswith(".osz")]

        for beatmap_path in beatmaps:
            osu_files.open_beatmap(beatmap_path)
