from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.core.window import Window
from kivy import properties as kp

from kivyrt.paths import load_kv
from kivyrt.subclasses import BgBoxLayout, BgBehavior

from kivymd.card import MDCard

from catalogue import CatalogueScreen


load_kv('search.kv', __file__)


location_query = 'distance(location, geopoint({}, {})) < 15000'


class SearchScreen(CatalogueScreen):
    location = kp.ListProperty()
    app_location = kp.ListProperty()
    query_string = kp.StringProperty()
    filters_open = kp.BooleanProperty(False)
    _anim_duration = kp.NumericProperty(.3)
    _first_search = kp.BooleanProperty(False)

    @property
    def location_query(self):
        return location_query.format(*self.location)

    def on_app_location(self, *args):
        if not self._first_search:
            self._app.restaurants.query(location_query.format(*self.app_location))
            self._first_search = True

    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.esc_handler)
        Window.bind(on_motion=self.close_filters)

    def close_filters(self, _, type_, touch):
        if type_ == 'end' and not self.collide_point(*touch.pos):
            self.filters_open = False

    def esc_handler(self, __, keycode1, *_):
        if self.get_parent_window() and keycode1 in [27, 1001]:
            if self.filters_open:
                self.filters_open = False
                return True
        return False

    @property
    def _app(self):
        return App.get_running_app()

    def search(self):
        self.filters_open = False
        self.ids.loading.opacity = 1
        query = self._query
        self._app.queries.post({'squery': query,
                                'made_from': str(self.app_location)})
        self._app.restaurants.query(query,
                                    on_success=self.show_summary,
                                    on_finished=self.hide_loading)

    @property
    def _query(self):
        components = (self.query_string, self.ids.tag_filter.query,
                      self.ids.price_filter.query, self.location_query)
        return ' AND '.join((component for component in components if component))

    def hide_loading(self, *args):
        self.ids.loading.opacity = 0

    def show_summary(self, *args):
        self.ids.catalogue.show_summary()


class FilterBase(MDCard):
    filter_id = kp.StringProperty()
    query = kp.StringProperty()
    _query_base = '{}'

    def clear(self):
        pass


class TagFilter(FilterBase):
    _query_base = 'tags: ({})'

    def clear(self):
        self.ids.ts.selected = []


class PriceFilter(FilterBase):
    _query_base = 'price: ({})'

    @property
    def price_buttons(self):
        return [self.ids['pb{}'.format(x)] for x in range(1, 5)]

    def calculate_query(self):
        prices = [str(pb.value) for pb in self.price_buttons if pb.state == 'down']
        query_options = ' OR '.join(prices)
        query = self._query_base.format(query_options) if query_options else ''
        self.query = query

    def clear(self):
        [setattr(pb, 'state', 'normal') for pb in self.price_buttons]



class PriceButton(BgBehavior, ToggleButton):
    value = kp.NumericProperty()

