import logging


def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level for the root logger
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w',
        encoding="utf-8"
    )
    file_handler = logging.FileHandler("app.log") 
    stdout_handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    stdout_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(stdout_handler)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)


def info(message: str):
    logging.getLogger().info(f"INFO: {message}")
    print(f"INFO: {message}")


def debug(message: str):
    logging.getLogger().debug(f"DEBUG: {message}")
    print(f"DEBUG: {message}")


def error(message: str):
    logging.getLogger().error(f"ERROR: {message}")
    print(f"ERROR: {message}")


def warn(message: str):
    logging.getLogger().warning(f"WARNING: {message}")
    print(f"WARNING: {message}")


def panic(message: str):
    logging.error(message)