import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
def create_browser():
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1280") # type: ignore
    options.add_argument("--height=805") # type: ignore
    options.set_preference("layers.acceleration.force-enabled", True)
    options.set_preference("gfx.webrender.all", True)
    options.add_argument("--log-level=fatal") #type: ignore
    options.set_preference("security.fileuri.strict_origin_policy", False)
    service = Service(log_output=os.devnull)
    # options.add_argument("--headless") # type: ignore
    browser = webdriver.Firefox(options=options, service=service)
    return browser