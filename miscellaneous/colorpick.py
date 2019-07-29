from kivy.config import Config

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

kv = """
<Test>:
    ColorWheel:
        _pieces_of_pie: 4
"""

class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

class TestApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    Builder.load_string(kv)
    TestApp().run()

