# src/automation/base_automation.py
class BaseAutomation:
    def __init__(self, driver):
        self.driver = driver

    def run(self):
        raise NotImplementedError("Subclasses must implement this method.")

