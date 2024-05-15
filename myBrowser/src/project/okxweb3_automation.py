import time

from myBrowser.src.project.browser_manager import BrowserManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OkxWeb3Automation(BrowserManager):

    def __init__(self, password, private_key=None, mnemonic=None, **kwargs):
        super().__init__(**kwargs)
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.password = password
        self.url = "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html"

    def first_import(self):
        self.driver.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html#initialize")
        button_import_css = "#app > div > div > div > div._affix_aopau_14 > div > div:nth-child(2) > button"
        button_private_css = "#app > div > div > div > div._main_kpxtk_12 > div:nth-child(2) > div > div._left_kpxtk_39"
        input_mnemonic_css = ("input.mnemonic-words-inputs__container__input")
        confirm_css = "button[type='submit']"
        input_password_css = "input.okui-input-input"
        button_not_css = "#app > div > div > div > div > div._affix_aopau_14 > div > button.okui-btn.btn-lg.btn-outline-secondary.block.mobile"
        button_open_css = "button.okui-btn.btn-lg.btn-fill-highlight.block.mobile"
        self.wait_for_element_to_be_visible((By.CSS_SELECTOR, button_import_css)).click()
        self.wait_for_element_to_be_visible((By.CSS_SELECTOR, button_private_css)).click()
        words = self.mnemonic.split(" ")
        if self.mnemonic is not None:
            inputs = self.driver.find_elements(By.CSS_SELECTOR, input_mnemonic_css)
            for i, word_input in enumerate(inputs):
                word_input.send_keys(words[i])
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, confirm_css))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, input_password_css))
        )
        inputs_password = self.driver.find_elements(By.CSS_SELECTOR, input_password_css)
        for i in inputs_password:
            i.send_keys(self.password)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, confirm_css))
        ).click()

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_not_css))
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, button_open_css))
        )
        self.driver.find_elements(By.CSS_SELECTOR, button_open_css)[1].click()

    def open(self):
        self.driver.get(self.url)

    def run(self):
        self.start()
        self.load_encrypt_from_index()
        self.first_import()
        self.close()


if __name__ == '__main__':
    from myBrowser.src.utils.eth_manager import EVMAddressManager
    evm_addr_manager = EVMAddressManager()
    okx = OkxWeb3Automation(user_data_index=600, password="123456", evm_addr_manager=evm_addr_manager)
    okx.run()
