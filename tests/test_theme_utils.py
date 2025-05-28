from src.shop_list.utils.theme_utils import save_theme, load_theme


def test_save_and_load_theme(tmp_path):
    # Переопределяем путь к файлу настроек на временный
    settings_file = tmp_path / 'settings.json'
    import src.shop_list.utils.theme_utils as theme_utils

    theme_utils.SETTINGS_FILE = str(settings_file)

    save_theme('Dark', 'DeepPurple')
    theme, palette = load_theme()
    assert theme == 'Dark'
    assert palette == 'DeepPurple'

    save_theme('Light', 'Blue')
    theme, palette = load_theme()
    assert theme == 'Light'
    assert palette == 'Blue'
