import kivy
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from config import logger
from config import DB_FULL_PATH
from src.shop_list.models.db import Database
from shop_list.utils.sql_utils import load_queries
from src.shop_list.utils.theme_utils import save_theme, load_theme


kivy.require('2.3.1')


QUERIES = load_queries('src/shop_list/models/qeuries.sql')


class ItemRow(MDBoxLayout):
    def __init__(self, item_id, name, bought, db, refresh_callback, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height='48dp', **kwargs)
        self.item_id = item_id
        self.name = name
        self.bought = bought
        self.db = db
        self.refresh_callback = refresh_callback

        self.checkbox = MDCheckbox(active=bool(bought))
        self.checkbox.bind(active=self.toggle_bought)

        self.label = MDLabel(text=name, halign='left')

        self.edit_button = MDIconButton(
            icon='pencil',
            theme_text_color='Primary',
            text_color=get_color_from_hex('#1976D2'),
            on_release=self.show_edit_dialog,
        )

        self.delete_button = MDIconButton(
            icon='delete', theme_text_color='Secondary', on_release=self.delete_item
        )

        self.add_widget(self.checkbox)
        self.add_widget(self.label)
        self.add_widget(self.edit_button)
        self.add_widget(self.delete_button)

    def toggle_bought(self, checkbox, value):
        self.query = QUERIES['UPDATE_BOUGHT']
        self.db.execute_query(self.query, (int(value), self.item_id))
        self.refresh_callback()

    def delete_item(self, *args):
        # Показываем диалог подтверждения
        self.confirm_dialog = MDDialog(
            title='Удалить элемент?',
            text=f'Вы уверены, что хотите удалить "{self.name}"?',
            buttons=[
                MDFlatButton(text='Нет', on_release=lambda x: self.confirm_dialog.dismiss()),
                MDFlatButton(text='Да', on_release=self.confirm_delete),
            ],
        )
        self.confirm_dialog.open()

    def confirm_delete(self, *args):
        self.confirm_dialog.dismiss()
        self.query = QUERIES['DELETE']
        self.db.execute_query(self.query, (self.item_id,))
        self.refresh_callback()

    def show_edit_dialog(self, *args):
        self.text_field = MDTextField(text=self.name)
        self.dialog = MDDialog(
            title='Редактировать',
            type='custom',
            content_cls=self.text_field,
            buttons=[
                MDFlatButton(text='Отмена', on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text='Сохранить', on_release=self.save_edit),
            ],
        )
        self.dialog.open()

    def save_edit(self, *args):
        self.query = QUERIES['UPDATE_NAME']
        new_name = self.text_field.text.strip()
        if new_name:
            self.db.execute_query(self.query, (new_name, self.item_id))
            self.label.text = new_name
            self.dialog.dismiss()
            self.refresh_callback()


class Root(MDScreen):
    def __init__(self, *args, **kwargs):
        logger.info('Ініціалізація головного екрану')
        self.db = Database(DB_FULL_PATH)
        self.db.execute_query(QUERIES['CREATE'])  # Создать таблицу, если нет
        super().__init__(*args, **kwargs)
        self.refresh_items()
        self.dialog = None

    def show_add_dialog(self):
        if self.dialog is None:
            self.text_field = MDTextField(hint_text='product')
            self.dialog = MDDialog(
                title='Add product',
                type='custom',
                content_cls=self.text_field,
                buttons=[
                    MDFlatButton(text='Cancel', on_release=lambda x: self.dialog.dismiss()),
                    MDFlatButton(text='Ok', on_release=self.save_item),
                ],
            )
        self.text_field.text = ''
        self.dialog.open()
        logger.debug('Діалог додавання відкрито')

    def save_item(self, *args):
        self.query = QUERIES['INSERT']
        logger.debug('Збереження елемента')
        name = self.text_field.text.strip()
        if name:
            self.db.execute_query(self.query, (name, 0))
            self.dialog.dismiss()
            self.refresh_items()

    def refresh_items(self):
        self.query = QUERIES['SELECT']
        self.ids.item_list.clear_widgets()
        items = self.db.get_all_items(self.query)
        for item in items:
            item_id, name, *rest = item
            bought = rest[0] if rest else 0
            row = ItemRow(item_id, name, bought, self.db, refresh_callback=self.refresh_items)
            self.ids.item_list.add_widget(row)

    def toggle_theme(self):
        new_theme = 'Dark' if self.theme_cls.theme_style == 'Light' else 'Light'
        new_palette = 'DeepPurple' if new_theme == 'Dark' else 'Blue'
        self.theme_cls.theme_style = new_theme
        self.theme_cls.primary_palette = new_palette
        save_theme(new_theme, new_palette)
        self.bg_color = self.get_bg_color()

    def get_bg_color(self):
        return (0.95, 0.95, 1, 1) if self.theme_cls.theme_style == 'Light' else (0.1, 0.1, 0.1, 1)


class ShopList(MDApp):
    def build(self) -> Root:
        theme, palette = load_theme()
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = palette
        self.title = 'Shopping'
        logger.info('Загружаю файл .kv')
        Builder.load_file('src/shop_list/views/ui.kv')
        root = Root()
        return root


if __name__ == '__main__':
    ShopList().run()
