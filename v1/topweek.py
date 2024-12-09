import os
import lib
from lib import logger


def main(arguments="de da ph pr"):
    config = lib.config.ConfigHandler().load_config()
    osu_session_handler = lib.osu.web.OsuSessionHandler()
    osu_folder_handler = lib.osu.local.OsuFolderHandler(config)
    queue_manager = lib.queue.QueueManager()
    skin_handler = lib.github.SkinHandler()

    osu_danser_handler = lib.danser.OsuDanserHandler(config)

    queue_manager.type_chooser(config_json=config, predefined_answer="")
    queue_manager.filter_queue("", "")

    queue_manager.get_replays_from_queue()
    queue_manager.download_beatmaps_from_queue(
        osu_session_handler, osu_folder_handler)
    queue_manager.verify_skins(osu_folder_handler, skin_handler)

    for queue_entry in queue_manager.queue:
        replay_handler = lib.replays.OsuReplayHandler(queue_entry)

        osu_request_handler = lib.osu.web.OsuRequestHandler(
            queue_entry, replay_handler.replay_info, queue_manager.has_updated_spreadsheet)

        osu_request_handler.get_beatmap()
        osu_request_handler.get_scores()
        osu_request_handler.get_player_info()

        beatmapset_path = osu_folder_handler.get_beatmapset_path_by_string(
            osu_request_handler.beatmap_info[0]["beatmapset_id"])
        replay_difficulty_path = osu_folder_handler.get_beatmapset_difficulty_by_string(
            beatmapset_path, osu_request_handler.beatmap_info[0]["version"])
        beatmap_background_path = osu_folder_handler.get_background_path_from_difficulty(
            beatmapset_path, osu_request_handler.beatmap_info[0]["version"])

        player_leaderboard_position = lib.osu.is_replay_at_leaderboard(
            replay_handler.replay_info, osu_request_handler.beatmap_scores)
        map_star_rating = lib.osu.calculate_star_rating(
            replay_difficulty_path, replay_handler.replay_info)
        play_pp = lib.osu.calculate_pp(
            replay_difficulty_path, replay_handler.replay_info)
        play_grade = lib.osu.calculate_grade(replay_handler.replay_info.number_300s,  replay_handler.replay_info.number_100s,
                                             replay_handler.replay_info.number_50s, replay_handler.replay_info.misses, replay_handler.replay_info.mod_combination)

        user_avatar_path = lib.osu.web.get_user_image(
            osu_request_handler.player_info[0]["user_id"])

        danser_output_path = os.path.join(
            config["Directories"]["Danser"], "videos", f"{queue_entry['replay_id']}.mp4")

        if "de" in arguments.lower():
            # Description
            lib.funreplays.create_description(queue_entry["replay_id"],
                                              osu_request_handler.player_info,
                                              osu_request_handler.beatmap_info,
                                              map_star_rating, play_pp,
                                              skin_handler.get_skin_by_name(
                                                  queue_entry["skin"])["link"],
                                              replay_handler, player_leaderboard_position)

        if "da" in arguments.lower():
            # Danser
            custom_danser_setting = osu_danser_handler.setup_custom_settings(
                cursor_size=float(queue_entry["cursor_size"]))
            danser_output_path = osu_danser_handler.record_replay(
                queue_entry["replay"], queue_entry["skin"], queue_entry["replay_id"], custom_setting=custom_danser_setting)

        if "ph" in arguments.lower():
            # Photoshop
            lib.photoshop.funreplays_edit(queue_entry["replay_id"],
                                          osu_request_handler.player_info[0]["username"],
                                          replay_handler.replay_info,
                                          play_pp,
                                          map_star_rating,
                                          osu_request_handler.beatmap_info[0]["version"],
                                          osu_request_handler.beatmap_info[0]["title"],
                                          player_leaderboard_position,
                                          beatmap_background_path,
                                          user_avatar_path)

        if "pr" in arguments.lower():
            # Premiere
            lib.premiere.funreplays_edit(danser_output_path, queue_entry["replay_id"], osu_request_handler.beatmap_info[0]["title"], osu_request_handler.beatmap_info[0]["version"], replay_handler.replay_info.number_300s,  replay_handler.replay_info.number_100s,  replay_handler.replay_info.number_50s,
                                         replay_handler.replay_info.misses, play_grade, lib.osu.calculate_accuracy(replay_handler.replay_info.number_300s,  replay_handler.replay_info.number_100s,  replay_handler.replay_info.number_50s,  replay_handler.replay_info.misses), play_pp, replay_handler.replay_info.max_combo)

    logger.info("Script finished", True)


if __name__ == "__main__":
    main("de da ph pr")
