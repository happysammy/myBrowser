import time

from myBrowser.src.project.browser_manager import BrowserManager


class CommonAutomation(BrowserManager):

    def __init__(self, user_data_index=None, **kwargs):
        super().__init__(user_data_index=user_data_index, **kwargs)

    def run(self):
        self.start()
