import kivy
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

kivy.require('2.3.1')


class Root(MDScreen):
    pass


class ShopList(MDApp):
    def build(self):
        self.title = 'Shopping'
        return Root()


if __name__ == '__main__':
    ShopList().run()
