from kivy.properties import (ListProperty, StringProperty, DictProperty,
                             BooleanProperty, NumericProperty)
from kivy import properties as kp
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.app import App

from kivyrt.paths import load_kv
from kivyrt.router import Router, route, route_options
from kivyrt.subclasses import BgBoxLayout, ButtonBoxLayout
from kivyrt.colors import colors
from kivyrt.texturebehavior import TextureBehavior

from kivymd.icon_definitions import md_icons

from owner import OwnerRouter
from search import SearchScreen
from favorites import FavoriteRouter
from about import AboutScreen


load_kv('mainrouter.kv', __file__)

route_icons = {'search': md_icons['magnify'],
               'about': md_icons['information'],
               'favorites': md_icons['star'],
               'owner': md_icons['account'],
               '': md_icons['language-python']}
route_colors = {'owner': 'LightBlue',
                'search': 'Red',
                'favorites': 'Amber',
                'about': 'LightGreen'}


_animation_time = .2


class MainRouter(Router):
    search_screen = kp.ObjectProperty()
    favorite_screen = kp.ObjectProperty()

    @route('owner')
    @route('owner/<path:subroute>')
    @route_options(with_view=True)
    def owner(self, view, subroute='/'):
        if not view:
            view = OwnerRouter()
        view.route = subroute
        return view

    @route('search')
    def search(self):
        if not self.search_screen:
            self.search_screen = SearchScreen()
        self.search_screen.clear()
        return self.search_screen

    @route('favorites')
    @route('favorites/<path:subroute>')
    @route_options(with_view=True)
    def favorites(self, view, subroute='/'):
        if not self.favorite_screen:
            self.favorite_screen = FavoriteRouter()
        self.favorite_screen.route = subroute
        return self.favorite_screen

    @route('about')
    def about(self):
        return AboutScreen()


class NavBar(TextureBehavior, BgBoxLayout):
    pass


class NavButton(ButtonBoxLayout):
    route = StringProperty()
    set_route = StringProperty()

    icon = StringProperty()

    isactive = BooleanProperty()
    _alpha = NumericProperty(1)

    app_color = ListProperty([0, 0, 0, 0])
    color = ListProperty([0, 0, 0, 0])

    def on_isactive(self, _, isactive):
        alpha = 1 * isactive
        color = self.app_color if isactive else colors.grey500
        Animation(_alpha=alpha, color=color, d=_animation_time).start(self)

    def on_route(self, _, route):
        self.icon = route_icons[route]

