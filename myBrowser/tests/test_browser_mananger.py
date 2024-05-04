import pytest
from myBrowser.src.project.browser_manager import BrowserManager
from selenium import webdriver


def test_init_driver(mocker):
    browser_manager = BrowserManager(base_config_name='test_config.yaml')
    mocker.patch('selenium.webdriver.Chrome')
    browser_manager.init_driver()
    webdriver.Chrome.assert_called_once()


def test_run_raises_not_implemented_error():
    browser_manager = BrowserManager(base_config_name='test_config.yaml')
    with pytest.raises(NotImplementedError):
        browser_manager.run()


def test_start(mocker):
    browser_manager = BrowserManager(base_config_name='test_config.yaml')
    mocker.patch.object(BrowserManager, 'init_driver')
    browser_manager.start()
    browser_manager.init_driver.assert_called_once()


def test_close_closes_driver(mocker):
    browser_manager = BrowserManager(base_config_name='test_config.yaml')
    browser_manager.driver = mocker.MagicMock()
    browser_manager.close()
    browser_manager.driver.quit.assert_called_once()

def test_load_extensions_with_crx_files(mocker):
    # Mocking the necessary functions and objects
    mocker.patch('myBrowser.src.project.browser_manager.os.walk', return_value=[
        ('/path/to/extensions', ['dir1', 'dir2'], ['file1.crx', 'file2.crx']),
        ('/path/to/extensions/dir1', [], ['file3.txt']),
        ('/path/to/extensions/dir2', [], [])
    ])

    options_mock = mocker.MagicMock()
    manager = BrowserManager(user_data_index=1)
    manager.load_extensions(options_mock)

    options_mock.add_extension.assert_any_call('/path/to/extensions/file1.crx')
    options_mock.add_extension.assert_any_call('/path/to/extensions/file2.crx')

def test_load_extensions_without_crx_files(mocker):
    # Mocking the necessary functions and objects
    mocker.patch('myBrowser.src.project.browser_manager.os.walk', return_value=[
        ('/path/to/extensions', ['dir1', 'dir2'], ['file1.txt']),
        ('/path/to/extensions/dir1', [], ['file2.txt']),
        ('/path/to/extensions/dir2', [], [])
    ])

    options_mock = mocker.MagicMock()
    manager = BrowserManager(user_data_index=1)
    manager.load_extensions(options_mock)

    options_mock.add_extension.assert_not_called()
