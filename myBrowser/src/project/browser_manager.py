import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import os
from myBrowser.src.utils.config_loader import load_base_config, load_browser_config, get_config_path


class BrowserManager:
    def __init__(self, user_data_index=None, base_config_name='config.yaml', excel_name='browsers_config.xlsx'):
        base_config_file_path = get_config_path(base_config_name)
        base_config = load_base_config(base_config_file_path)
        self.driver_path = base_config['driver_path']
        self.user_data_base_path = base_config['user_data_base_path']

        self.user_data_index = user_data_index
        excel_browser_config_path = get_config_path(excel_name)
        self.browser_config = load_browser_config(excel_browser_config_path, user_data_index)

        self.driver = None
        self.start()

    def start(self):
        self.driver = self.init_driver()

    def init_driver(self):
        options = webdriver.ChromeOptions()
        for option in self.browser_config.get('options', []):
            options.add_argument(option)
        if self.browser_config.get('proxy'):
            options.add_argument(f'--proxy-server={self.browser_config["proxy"]}')
        if self.user_data_index is not None:
            user_data_dir = os.path.join(self.user_data_base_path, str(self.user_data_index))
            options.add_argument(f'--user-data-dir={user_data_dir}')
        service = ChromeService(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def close(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    manager = BrowserManager(user_data_index=1)
    time.sleep(30)
    # 执行操作
    manager.close()