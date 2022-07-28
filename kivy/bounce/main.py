import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.properties import ListProperty, Clock
from kivy.uix.widget import Widget

class Bounce(Widget):
    circle_pos = ListProperty([400,400])
    circle_size = ListProperty([100,100])
    color = ListProperty([1,0,0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60)  # 60 fps
        self.vx = 10
        self.vy = 10
        self.size_x, self.size_y = self.circle_size

    def on_size(self, *args):
        print(f'Height: {str(self.height)}, Width: {self.width}')
        self.circle_pos = [self.center_x-self.size_x/2, self.center_y-self.size_y/2]

    def update(self, dt):
        x, y = self.circle_pos
        x += self.vx
        y += self.vy
        r, g, b = self.color

        if ((x+self.size_x) >= self.width):
            x = self.width - self.size_x
            self.vx = -self.vx
            self.color = [1-r, g, 1-b]

        if x <= 0:
            x = 0
            self.vx = -self.vx
            self.color = [1-r, g, 1-b]

        if ((y+self.size_y) >= self.height):
            y = self.height - self.size_y
            self.vy = -self.vy
            self.color = [1-r, 1-g, b]

        if y <= 0:
            y = 0
            self.vy = -self.vy
            self.color = [1-r, 1-g, b]

        self.circle_pos = [x, y]


class BounceApp(App):
    pass

BounceApp().run()