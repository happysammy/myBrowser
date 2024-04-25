import pytest
from myBrowser.src.project.browser_manager import BrowserManager
from selenium import webdriver

def test_init_driver(mocker):
    browser_manager = BrowserManager(config_path='test_config.json')
    mocker.patch('selenium.webdriver.Chrome')
    browser_manager.init_driver()
    webdriver.Chrome.assert_called_once()

def test_run_raises_not_implemented_error():
    browser_manager = BrowserManager(config_path='test_config.json')
    with pytest.raises(NotImplementedError):
        browser_manager.run()

def test_start(mocker):
    browser_manager = BrowserManager(config_path='test_config.json')
    mocker.patch.object(BrowserManager, 'init_driver')
    browser_manager.start()
    browser_manager.init_driver.assert_called_once()

def test_close_closes_driver(mocker):
    browser_manager = BrowserManager(config_path='test_config.json')
    browser_manager.driver = mocker.MagicMock()
    browser_manager.close()
    browser_manager.driver.quit.assert_called_once()
