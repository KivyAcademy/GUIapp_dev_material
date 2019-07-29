from kivy.uix.screenmanager import Screen

from kivyrt.paths import load_kv


load_kv('about.kv', __file__)


class AboutScreen(Screen):
    pass

