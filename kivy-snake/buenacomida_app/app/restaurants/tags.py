from kivy.uix.stacklayout import StackLayout
from kivy.properties import (ListProperty, StringProperty, DictProperty,
                             NumericProperty, BooleanProperty)
from kivy.uix.button import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout

from kivymd.button import CircularRippleBehavior

from kivyrt.dataview import DataBehavior, SelectionBehavior
from kivyrt.paths import load_kv


load_kv('tags.kv', __file__)


class TagSelector(DataBehavior, StackLayout):
    selected = ListProperty()


class Tag(FloatLayout):
    name = StringProperty()
    translated = StringProperty()
    translation = DictProperty()
    selected = BooleanProperty()
    source = StringProperty()
    language = StringProperty()

    def on_name(self, *args):
        self.on_language()

    def on_language(self, *args):
        try:
            self.translated = self.translation[self.language]
        except:
            self.translated = self.name

    _label_width  = NumericProperty(0)
    _image_width  = NumericProperty(0)


class TagButton(CircularRippleBehavior, SelectionBehavior, ButtonBehavior, Tag):
    pass

