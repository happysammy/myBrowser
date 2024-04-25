import os
import pytest
from myBrowser.src.utils.config_loader import load_config, get_config_path

# 假设你的测试配置文件名为test_config.json，并且放在tests目录下
TEST_CONFIG_PATH = '/Users/a1/scientist/myBrowser/myBrowser/config.json'


def test_get_config_path():
    expected_path = TEST_CONFIG_PATH
    # 如果你的get_config_path函数需要调整以指向测试配置文件，请在此处做相应修改
    actual_path = get_config_path()
    assert actual_path == expected_path, "get_config_path should return the correct path to config.json"

def test_load_config():
    config = load_config(TEST_CONFIG_PATH)
    assert isinstance(config, dict), "load_config should return a dictionary"

