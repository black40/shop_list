import json
import os

SETTINGS_FILE = 'settings.json'


def save_theme(theme_name: str, palette: str):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'theme': theme_name, 'palette': palette}, f)


def load_theme():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('theme', 'Light'), data.get('palette', 'Blue')
    return 'Light', 'Blue'
