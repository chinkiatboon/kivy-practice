import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class TestWidget(BoxLayout):
    pass

class testApp(App):
    pass

testApp().run()