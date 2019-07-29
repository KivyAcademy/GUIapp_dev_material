from kivyrt.subclasses import BgBoxLayout
from kivyrt.dataview import DataBox

from kivy import properties as kp
from kivy.animation import Animation
from kivy.uix.screenmanager import NoTransition

_summary_kv_string = '''
<SummaryList>
    viewclass: 'RestaurantSummary'
    bgcolor: colors.white
    height: (self.max_height * hidebox.height_alpha) or self.minimum_height
    size_hint_y: None
    orientation: 'vertical'
    ScreenManager
        id: sm
        size_hint_y: None
        height: root.height if root._is_open else closed_box.height
        transition: root._screenmanager_transition
        Screen
            opacity: (not root._is_open) * 1
            name: 'closed'
            BoxLayout
                id: closed_box
                orientation: vertical
                height: self.minimum_height
                size_hint_y: None
                ButtonBoxLayout
                    height: self.minimum_height
                    orientation: vertical
                    size_hint_y: None
                    height: dp(40)
                    padding: dp(8)
                    on_release: root.open()
                    MDLabel
                        text: root.show_text
                        color: 0, 0, 0, 1
                        text_size: self.size
                        halign: 'left'
                RecycleView
                    size_hint_y: None
                    height: rv_2.height
                    data: [root._current_data]
                    RecycleGridLayout
                        id: rv_2
                        size_hint_y: None
                        cols: 1
                        height: 0
                        on_minimum_height: Animation(height=self.minimum_height, d=root._anim_duration).start(self)
                        viewclass: root.viewclass
                        default_size_hint: root.default_size_hint
                        default_size: root.default_size
        Screen
            name: 'open'
            HideBox
                on_close: root.close()
                scroll: rv
                id: hidebox
                RecycleView
                    data: root.data
                    id: rv
                    RecycleGridLayout
                        cols: 1
                        size_hint_y: None
                        height: self.minimum_height + dp(60)
                        viewclass: root.viewclass
                        default_size_hint: root.default_size_hint
                        default_size: root.default_size
                NoFloatLayout
                    MDFloatingActionButton
                        id: fab
                        right: root.right - dp(20)
                        top: dp(80) * hidebox.height_alpha
                        icon: 'map'
                        on_release: root.open = False
'''


class SummaryList(BgBoxLayout):
    data = ListProperty()
    viewclass = StringProperty('')
    default_size = ListProperty([None, None])
    default_size_hint = ListProperty([1, 1])

    _is_open = kp.BooleanProperty(False)
    current_key = kp.StringProperty()
    _current_data = kp.DictProperty()
    _current_screen = kp.StringProperty()
    _key_name = kp.StringProperty('key')

    show_text = kp.StringProperty()

    max_height = kp.NumericProperty(0)
    _alpha = kp.NumericProperty(0)
    _anim_duration = kp.NumericProperty(.2)

    def __init__(self, **kwargs):
        super(SummaryList, self).__init__(**kwargs)
        self.bind(data=self._reset_scroll)
        self.bind(_is_open=self._change_screen)
        self._screenmanager_transition = NoTransition()

        self.bind(current_key=self._set_current_data)
        self.bind(_key_name=self._set_current_data)

    def _change_screen(self, *args):
        self.ids.sm.current = 'open' if self._is_open else 'closed'

    def _set_current_data(self, *args):
        for data in self.data:
            if self.data[self._key_name] == self.current_key
                self._current_data = data
                return

    def _handle_touch_up(self, *args):
        touch = args[1]
        collides = self.collide_point(*touch.pos)
        total_movement = abs(touch.osy - touch.sy) + abs(touch.osx - touch.sx)
        time = touch.time_end - touch.time_start
        if not collides and total_movement < .05 and time < .15:
            self.current_key = ''

    def _reset_scroll(self, *args):
        self.scroll.scroll_y = 1

    def open(self):
        self._is_open = True
        self._animate_state()

    def open(self):
        self._animate_state(on_complete=setattr(self, '_is_open', False))

    def _animate_state(self, open, **kwargs):
        self._reset_scroll()
        a = Animation(_alpha=(1 * self._is_open), d=self._anim_duration).start(self.ids.hidebox)
        a.bind(**kwargs)

Builder.load_string(_summary_kv_string)

