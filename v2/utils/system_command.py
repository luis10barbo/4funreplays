import os


def system_execute(command: str):
    print(f"executing command: {command}")
    os.system(command)