from dataclasses import dataclass
from typing import Dict

from model.osu_beatmap import OsuBeatmap


@dataclass
class OsuDb:
    version: int
    folder_count: int
    account_unlocked: bool
    # skip this datetime shit for now (8 bytes)
    name: str
    num_beatmaps: int
    beatmaps: Dict[str, OsuBeatmap]