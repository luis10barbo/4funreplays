from lib import *

config = config.ConfigHandler().load_config()

osu_folder = osu.local.files.OsuFolderHandler()

osu_folder.load_path_from_config(config)

search = osu_folder.get_beatmapset_path_by_string("1170697")
search = osu_folder.get_background_path_from_difficulty(search[0], "Ecstasy")

search = osu_folder.get_beatmapset_path_by_string("Roge")
search = osu_folder.get_background_path_from_difficulty(search[0], "Voce E Feia")

google_spreadsheet = queue.GoogleSpreadsheetHandler()
google_spreadsheet.get_spreadsheet_id_from_config(config)
google_spreadsheet.get_queue_from_google()

