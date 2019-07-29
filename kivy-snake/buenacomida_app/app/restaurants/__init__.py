# -*- coding: utf-8 -*-
from kivy import properties as kp
from kivy.app import App
from kivy.clock import Clock

from kivyrt.paths import load_kv
from kivyrt.subclasses import BgBoxLayout, HeightlessBox, BgBehavior

from kivymd.card import MDCard


load_kv('restaurants.kv', __file__)


class GVMDCard(BgBehavior, MDCard):
    pass


class RestaurantCapture(BgBoxLayout):
    pass


class TagCapture(GVMDCard):
    pass


class PriceCapture(HeightlessBox):
    price_range = kp.NumericProperty()
    _price_range = kp.ListProperty([0])


class UrlCapture(HeightlessBox):
    pass


class LocationCapture(GVMDCard):
    def __init__(self, **kwargs):
        super(LocationCapture, self).__init__(**kwargs)
        Clock.schedule_once(self._center_on_app_location)

    def _center_on_app_location(self, *args):
        self.ids.map_.center_on(*App.get_running_app().location_handler.location)

