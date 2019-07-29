from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy import properties as kp
from kivy.core.window import Window
from kivy.clock import Clock

from kivyrt.paths import load_kv
from kivyrt.network.datastore import urlencode
from kivyrt.network.urlreq import SUrlRequest

from catalogue import summary_list


load_kv('catalogue.kv', __file__)


class Catalogue(Screen):
    _search_url = 'https://maps.googleapis.com/maps/api/geocode/json?{}' \
                  '&key=AIzaSyDVVAh1A6H2wjgB6JEHpAhu3BDaD1_Jjr0'
    active = kp.BooleanProperty(False)
    data = kp.ListProperty()

    def __init__(self, **kwargs):
        super(Catalogue, self).__init__(**kwargs)
        Clock.schedule_once(self.center_map_on_location)

        Window.bind(on_keyboard=self.esc_handler)

    @property
    def _app(self):
        return App.get_running_app()

    def center_map_on_location(self, *args):
        # center map on apps location
        self.ids._map.center_on(*App.get_running_app().location)

    def esc_handler(self, __, keycode1, *_):
        if self.get_parent_window() and keycode1 in [27, 1001]:
            if self.ids.summary_list._is_open:
                self.close()
                return True
            if self.ids.summary_list.current_key:
                self.clear()
                return True
        return False

    def go_to(self, text):
        place = urlencode({'address': text})
        SUrlRequest(self._search_url.format(place),
                    on_success=self._process_goto_result)

    def _process_goto_result(self, req, res):
        try:
            location = res['results'][0]['geometry']['location']
            lat = location['lat']
            lon = location['lng']
            self.ids._map.zoom = 14
            self.ids._map.center_on(lat, lon)
        except:
            self._app.notify('No results found!')

    def clear(self):
        self.ids.summary_list.current_key = ''
        self.close()

    def close(self):
        self.ids.summary_list.close()

    def show_summary(self):
        self.ids.summary_list.open()

    def show_detail(self, key):
        self.ids.summary_list.open_detail(key)


class CatalogueScreen(Screen):
    def clear(self):
        self.ids.catalogue.clear()

