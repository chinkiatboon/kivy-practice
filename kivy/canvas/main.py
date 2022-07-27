import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.widget import Widget

class CanvasExample(Widget):
    rect_pos = ListProperty([400,400])
    def move_rectangle(self, rect):
        x, y = self.rect_pos
        x = x + 30
        if x > self.width-150:
            self.rect_pos = [self.width-150,y]
        else:
            self.rect_pos = [x,y]

class CanvasApp(App):
    pass

CanvasApp().run()