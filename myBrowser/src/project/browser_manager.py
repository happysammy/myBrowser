from myBrowser.src.utils.config_loader import load_config,get_config_path
from selenium import webdriver
import os

class BrowserManager:
    driver: webdriver.Chrome
    def __init__(self, config_path=None):
        if config_path == None:
            config_path = get_config_path()
        self.config = load_config(config_path)
        self.driver_path = self.config.get('driver_path')
        self.options = self.config.get('options', [])
        self.driver = None
        self.start()

    def start(self):
        self.driver = self.init_driver()

    def init_driver(self):
        options = webdriver.ChromeOptions()
        for option in self.options:
            options.add_argument(option)

        service = webdriver.ChromeService(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def close(self):
        if self.driver:
            self.driver.quit()
