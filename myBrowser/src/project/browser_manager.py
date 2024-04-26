from myBrowser.src.utils.config_loader import load_config, get_config_path
from selenium import webdriver
import os

class BrowserManager:
    driver: webdriver.Chrome

    def __init__(self, user_data_index=None, config_path=None):
        if config_path is None:
            config_path = get_config_path()
        self.config = load_config(config_path)
        self.driver_path = self.config.get('driver_path')
        self.options = self.config.get('options', [])
        self.user_data_base_path = self.config.get('user_data_base_path')  # 假设配置中有用户数据目录的基路径
        self.user_data_index = user_data_index  # 用户数据目录的序号
        self.driver = None
        self.start()

    def start(self):
        self.driver = self.init_driver()

    def init_driver(self):
        options = webdriver.ChromeOptions()
        for option in self.options:
            options.add_argument(option)

        # 如果提供了user_data_index，则设置用户数据目录
        if self.user_data_index is not None:
            user_data_dir = os.path.join(self.user_data_base_path, str(self.user_data_index))
            options.add_argument(f'--user-data-dir={user_data_dir}')

        service = webdriver.ChromeService(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def close(self):
        if self.driver:
            self.driver.quit()

