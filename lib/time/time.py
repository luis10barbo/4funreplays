from datetime import datetime, timedelta

default_formatting = "%Y-%d-%m %H.%M.%S"

def get_formatting(spaces:str = True) -> str:
    formatting = default_formatting
    if spaces == False:
        formatting = formatting.replace(" ", "_")
    return formatting

def get_current_time_computer(spaces:bool = True) -> datetime:
    return datetime.now().strftime(get_formatting(spaces))

def time_from_string(string:str, spaces:bool = True) -> datetime:
    return datetime.strptime(string, get_formatting(spaces))

def string_from_time(time:datetime, spaces:bool = True) -> str:
    return datetime.strftime(time, get_formatting(spaces))

def time_from_seconds(seconds:float) -> datetime:
    return datetime.fromtimestamp(seconds)