# src/utils/config_loader.py
import json
import os
import yaml
import pandas as pd


def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def get_config_path(config_filename):
    # 获取当前文件的绝对路径
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # 向上回溯两级到项目根目录（根据你的项目结构调整）
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    # 构建config.json的绝对路径
    config_path = os.path.join(root_dir, config_filename)
    return config_path


def load_base_config(config_path):
    """从YAML文件加载基础配置"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def load_browser_config(excel_path, user_data_index):
    """从Excel文件加载特定Index的浏览器配置"""
    df = pd.read_excel(excel_path)
    config_row = df.loc[df['Index'] == user_data_index]
    if not config_row.empty:
        options = config_row.iloc[0]['Options'].split(';') if pd.notna(config_row.iloc[0]['Options']) else []
        proxy = config_row.iloc[0]['Proxy'] if pd.notna(config_row.iloc[0]['Proxy']) else None
        return {'options': options, 'proxy': proxy}
    else:
        return {'options': [], 'proxy': None}
