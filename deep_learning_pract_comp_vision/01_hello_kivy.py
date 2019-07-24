import kivy.app
import kivy.uix.label
import kivy.uix.boxlayout
class FirstApp(kivy.app.App):
    def build(self):
        self.label = kivy.uix.label.Label(text="Hello Kivy")
        self.layout = kivy.uix.boxlayout.BoxLayout()
        self.layout.add_widget(widget=self.label)
        return self.layout

firstApp = FirstApp()
firstApp.run()
