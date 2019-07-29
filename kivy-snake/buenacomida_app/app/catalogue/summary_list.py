from kivy import properties as kp
from kivy.animation import Animation
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy.app import App

from kivyrt.subclasses import BgBoxLayout, ButtonBoxLayout, HeightlessBox
from kivyrt.hide_behavior import HideBox
from kivyrt.paths import load_kv
from kivyrt.dataview import DataBehavior
from kivyrt.interface import InterfaceBehavior
from kivyrt.forms import FormBehavior

from mapview import MapMarker


load_kv('summary_list.kv', __file__)


class SummaryList(BgBoxLayout):
    _is_open = kp.BooleanProperty(False)
    data = kp.ListProperty()
    default_size = kp.ListProperty([None, None])
    default_size_hint = kp.ListProperty([1, 1])
    _extra_kwargs = kp.DictProperty()

    _anim_duration = kp.NumericProperty(.15)

    current_key = kp.StringProperty()
    detail_key = kp.StringProperty()
    _current_screen = kp.StringProperty()
    hidebox_screen = kp.StringProperty('summary')

    show_text = kp.StringProperty()

    max_height = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super(SummaryList, self).__init__(**kwargs)
        self.bind(data=self._reset_scroll)
        self.bind(_is_open=self._change_screen)
        self._screenmanager_transition = NoTransition()

        Clock.schedule_once(self.close)

    def _change_screen(self, *args):
        self.ids.sm.current = 'open' if self._is_open else 'closed'

    def open(self, *args):
        self.ids.hidebox.open()

    def open_detail(self, key=None):
        self.detail_key = key or self.current_key
        self.ids.sm_hidebox.current = 'detail'
        self.open()

    def close(self, *args):
        self.ids.hidebox.close()

    def _reset_scroll(self, *args):
        self.ids.hidebox._reset_scroll()


class RestaurantSummary(ButtonBoxLayout):
    name = kp.StringProperty()
    rating = kp.StringProperty()
    price = kp.StringProperty()
    stars = kp.StringProperty()
    tags = kp.StringProperty()
    address = kp.StringProperty()
    thumbnail = kp.StringProperty()
    key = kp.StringProperty()


class DataCarousel(DataBehavior, Carousel):
    pass


class RestaurantDetail(InterfaceBehavior, BgBoxLayout):
    images = kp.ListProperty()
    name = kp.StringProperty()
    phone_number = kp.StringProperty()
    rating = kp.StringProperty()
    website = kp.StringProperty()
    stars = kp.StringProperty()
    tags = kp.StringProperty()
    address = kp.StringProperty()
    key = kp.StringProperty()
    description = kp.StringProperty()
    favorite = kp.BooleanProperty()
    comment = kp.DictProperty()

    def add_or_remove_from_favorites(self):
        app = App.get_running_app()
        favorites = app.user.cache.get('favorites', [])
        if self.favorite:
            favorites.remove(self.key)
        else:
            favorites.append(self.key)
        app.user.put({'favorites': favorites})


class RestaurantMarker(MapMarker):
    callback = kp.ObjectProperty()
    key = kp.StringProperty()


class CommentSection(ScreenManager):
    restaurant_key = kp.StringProperty()
    your_comment = kp.DictProperty()

comment_defaults = {'text': {'error': False},
                    'slider': {}}

class MakeComment(FormBehavior, BgBoxLayout):
    defaults = comment_defaults
    key = kp.StringProperty()

    def verify_data(self, data, defaults):
        if not data['text']:
            defaults['text']['focus'] = True
            return defaults
        if data['text'] and data['rating'] and data['owner'] and data['restaurant']:
            self.ready = True
            data['text'] = data['text'].strip()
            data['rating'] = int(data['rating'])
            self.processed = data
            defaults['text']['text'] = ''
            defaults['slider']['value'] = 0
            self.dispatch('on_execute')
        return defaults


class Comment(InterfaceBehavior, ButtonBoxLayout):
    key = kp.StringProperty()
    text = kp.StringProperty()
    commenter = kp.StringProperty()
    created = kp.StringProperty()
    stars = kp.StringProperty()
    rating = kp.StringProperty()
    your_text = kp.StringProperty()


class YourComment(Comment):
    pass


