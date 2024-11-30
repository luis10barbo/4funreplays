import os
from model.config import Config
from utils.system_command import system_execute

def record(config: Config, replay_path: str, output_name: str):
    print(f"recording {replay_path} as {output_name}")
    if config is None:
        return
    
    record_command = f"{os.path.join(config["danser_path"], "danser-cli.exe")} -record -settings {config["danser_config"]} -replay {replay_path} -out {output_name}"
    system_execute(record_command)