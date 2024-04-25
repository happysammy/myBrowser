# src/utils/config_loader.py
import json
import os


def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def get_config_path():
    # 获取当前文件的绝对路径
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 向上回溯两级到项目根目录（根据你的项目结构调整）
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    # 构建config.json的绝对路径
    config_path = os.path.join(root_dir, 'config.json')
    return config_path
