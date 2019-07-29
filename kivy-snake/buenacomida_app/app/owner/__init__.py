from kivy.uix.screenmanager import Screen
from kivy import properties as kp

from kivyrt.paths import load_kv
from kivyrt.router import Router, route
from kivyrt.subclasses import HeightlessBox

from restaurants import RestaurantCapture
from login import LoginScreen


load_kv('owner.kv', __file__)


class OwnerRouter(Router):
    @route('/login')
    def login(self):
        return LoginScreen()

    @route('/profile')
    def profile(self):
        return ProfileScreen()

    @route('/capture')
    def capture(self):
        return RestaurantCapture()


class MyRestaurants(Screen):
    pass


class ProfileScreen(Screen):
    pass


class SearchBar(HeightlessBox):
    search = kp.StringProperty('')

