import time
import socket
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from myBrowser.src.utils.config_loader import load_base_config, load_browser_config, get_config_path
from myBrowser.src.utils.eth_manager import EVMAddressManager


class BrowserManager:
    driver: Optional[webdriver.Chrome]

    def __init__(self, user_data_index=None, base_config_name='config.yaml', excel_name='browsers_config.xlsx',
                 timeout=10):
        self.wait = None
        base_config_file_path = get_config_path(base_config_name)
        base_config = load_base_config(base_config_file_path)
        self.driver_path = base_config['driver_path']
        self.debug = base_config['debug']
        self.user_data_base_path = base_config['user_data_base_path']

        self.user_data_index = user_data_index
        excel_browser_config_path = get_config_path(excel_name)
        self.browser_config = load_browser_config(excel_browser_config_path, user_data_index)

        self.extensions_path = get_config_path(base_config.get('extensions_path', None))

        self.driver = None
        self.addr = None
        self.timeout = timeout

    def load_encrypt_from_index(self, evm_addr_manager: EVMAddressManager):
        """
        addr example {index:0,addr:0xaaa,private_key:0xaaa,mnemonic:word word}
        :param evm_addr_manager:
        :return:
        """
        self.addr = evm_addr_manager.get_address_info(self.user_data_index)
        if self.addr is None:
            return False
        else:
            return True


    def wait_for_element_to_be_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def start(self):
        if self.debug and self.is_port_available(9222):
            self.driver = self.init_driver_with_debug()
        elif self.debug:
            self.driver = self.connect_to_existing_driver()
        else:
            self.driver = self.init_driver()
            
        self.wait = WebDriverWait(self.driver, self.timeout)

    def is_port_available(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0

    def init_driver_with_debug(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--remote-debugging-port=9222")
        return self.init_driver(options)

    def connect_to_existing_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        return webdriver.Chrome(options=options, service=ChromeService(executable_path=self.driver_path))

    def init_driver(self, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
        if self.extensions_path:
            self.load_extensions(options)
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

    def load_extensions(self, options):
        """遍历extensions_path中的所有文件夹，加载CRX插件"""
        for root, dirs, files in os.walk(self.extensions_path):
            for file in files:
                if file.endswith('.crx'):
                    crx_path = os.path.join(root, file)
                    options.add_extension(crx_path)

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def close(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    manager = BrowserManager(user_data_index=None)
    manager.start()
    manager.driver.get("http://www.qq.com")
    time.sleep(30)
    # 执行操作
    #manager.close()
