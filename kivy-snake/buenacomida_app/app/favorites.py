from kivy.uix.screenmanager import Screen
from kivy import properties as kp
from kivy.app import App

from kivyrt.paths import load_kv
from kivyrt.router import Router, route

from catalogue import CatalogueScreen


load_kv('favorites.kv', __file__)


class FavoriteRouter(Router):
    favorite_screen = kp.ObjectProperty()
    favorites = kp.ListProperty()

    def on_favorites(self, *args):
        if not self.favorites:
            app = App.get_running_app()
            if app.mainroute == 'favorites':
                app.route = 'favorites/empty'

    @route('/')
    def show_favorites(self):
        if not self.favorite_screen:
            self.favorite_screen = FavoriteScreen()
        return self.favorite_screen

    @route('/empty')
    def empty(self):
        return EmptyFavorites()


class FavoriteScreen(CatalogueScreen):
    pass


class EmptyFavorites(Screen):
    pass

