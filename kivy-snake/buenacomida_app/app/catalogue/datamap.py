from kivyrt.dataview import DataBehavior
from kivy import properties as kp

from mapview import MapView


_tap_time = .2
_max_distance = .1

def _is_tap(touch):
    if touch.time_end - touch.time_start > _tap_time:
        return False
    if abs(touch.osy - touch.sy) + abs(touch.osx - touch.sx) > _max_distance:
        return False
    return True


class DataMap(MapView, DataBehavior):
    clear_callback = kp.ObjectProperty()

    def on_touch_up(self, touch):
        if _is_tap(touch):
            self.clear_callback()
        super(DataMap, self).on_touch_up(touch)

