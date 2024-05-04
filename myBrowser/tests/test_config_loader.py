import os
import pytest
import yaml

from myBrowser.src.utils.config_loader import load_config, get_config_path, load_base_config, load_browser_config

# 假设你的测试配置文件名为test_config.json，并且放在tests目录下
TEST_CONFIG_PATH = '/Users/a1/scientist/myBrowser/myBrowser/config.json'


def test_get_config_path():
    expected_path = TEST_CONFIG_PATH
    # 如果你的get_config_path函数需要调整以指向测试配置文件，请在此处做相应修改
    actual_path = get_config_path("config.json")
    assert actual_path == expected_path, "get_config_path should return the correct path to config.json"

def test_load_config():
    config = load_config(TEST_CONFIG_PATH)
    assert isinstance(config, dict), "load_config should return a dictionary"

def test_load_base_config_valid_yaml(tmp_path):
    # Create a temporary YAML file with valid content
    config_path = tmp_path / "valid_config.yaml"
    with open(config_path, 'w') as file:
        file.write("key: value")

    # Test loading the valid YAML file
    assert load_base_config(config_path) == {"key": "value"}

def test_load_base_config_invalid_yaml(tmp_path):
    # Create a temporary YAML file with invalid content
    config_path = tmp_path / "invalid_config.yaml"
    with open(config_path, 'w') as file:
        file.write("invalid_yaml: !!python/object/apply:os.system ['echo HACKED']")

    # Test loading the invalid YAML file
    with pytest.raises(yaml.YAMLError):
        load_base_config(config_path)

def test_path_base_config_yaml():
    config_path = get_config_path("config.yaml")
    config = load_base_config(config_path)

    assert config.get('extensions_path') == "./extensions/"
    extension_path = get_config_path(config.get("extensions_path"))
    assert extension_path == "/Users/a1/scientist/myBrowser/myBrowser/./extensions/"



def test_load_base_config_non_existent_file():
    # Test loading a non-existent file
    with pytest.raises(FileNotFoundError):
        load_base_config("non_existent_file.yaml")
