# -*- coding: utf-8 -*-
from collections import defaultdict

from kivy.properties import DictProperty, StringProperty
from kivy.loader import Loader

from kivyrt.storage.autosavestore import AutosaveStore
from kivyrt.translation import Translator
from kivyrt.network.datastore import (ConfiguratorModel, OwnedDatastoreModel,
                                      DatastoreModel)
from kivyrt.locationhandler import LocationHandler
from kivyrt.router import AppRouter

from kivymd.theming import ThemeManager
from kivymd.snackbar import Snackbar

from mainrouter import MainRouter, route_colors
from search import location_query


class Buenacomida(AppRouter):
    theme_cls = ThemeManager()
    mainroute = StringProperty()

    def on_route(self, _, route):
        self.mainroute = route.split('/')[0]
        return super(Buenacomida, self).on_route(_, route)

    def on_start(self):
        Loader.loading_image = 'res/search.zip'

    def on_mainroute(self, *args):
        self.theme_cls.primary_palette = self.route_colors[self.mainroute]

    def __init__(self, **kwargs):
        super(Buenacomida, self).__init__(**kwargs)

        self.route_colors = defaultdict(lambda: self.theme_cls.primary_palette)
        self.route_colors.update(route_colors)

        self.location_handler = LocationHandler()
        self.location = self.location_handler.location

        #self.markers = defaultdict(lambda: BuenMarker())

        self.translator = Translator('translation.json', 'espanol')

        self.user = ConfiguratorModel('https://buena-comida.appspot.com')
        self.restaurants = OwnedDatastoreModel(self.user, 'restaurants')
        self.comments = OwnedDatastoreModel(self.user, 'comments')
        self.brands = DatastoreModel(self.user, 'brands')
        self.tags = DatastoreModel(self.user, 'tags')
        self.queries = DatastoreModel(self.user, 'queries')

        self.storage = AutosaveStore('storage.json', ('cache', 'headers'), self.user)

        self.tags.get()

    def notify(self, text, translate=True):
        Snackbar(text=text).show()

    def build(self):
        self.root = MainRouter()
        self.route = 'search'
        return self.root


if __name__ == '__main__':
    Buenacomida().run()

