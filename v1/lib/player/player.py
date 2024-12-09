import json
from lib.paths import PLAYER_CONFIGS
from lib import logger


def update_player_config(profile_id: str, skin="", cursor_size=""):
    print(profile_id)
    if type(profile_id) != int:
        if profile_id.isnumeric() == False:
            logger.error(
                f"Profile id {profile_id} is not a number, player config not updated")
            return
        else:
            profile_id = int(profile_id)

    with open(PLAYER_CONFIGS, "r") as file:
        configs = json.load(file)

    configs[profile_id] = {
        "skin": skin,
        "cursor_size": cursor_size
    }

    with open(PLAYER_CONFIGS, "w") as file:
        json.dump(configs, file)


def get_player_config(profile_id: str):
    if profile_id.isnumeric() == False:
        logger.error(
            f"Profile id {profile_id} is not a number, player config not retrieved")
        return

    with open(PLAYER_CONFIGS, "r") as file:
        configs = json.load(file)

        if profile_id in configs:
            return configs[profile_id]
        else:
            logger.error(
                f"Profile id {profile_id} configs not found at playerconfigs.json")
