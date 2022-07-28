import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    NUM_LINES = 7       # Best to use odd numbers for there to be a centre line
    LINE_SPACING = 0.1  # Percentage instead of numeric figure

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    vertical_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_vertical_lines()

    def on_size(self, *args):
        print(f'Height: {str(self.height)}, Width: {self.width}')
        self.update_line()

    def on_perspective_point_x(self, widget, value):
        pass

    def on_perspective_point_y(self, widget, value):
        pass

    def initialize_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.NUM_LINES):
                self.vertical_lines.append(Line())

    def update_line(self):
        offset = -(int(self.NUM_LINES/2))

        for line in self.vertical_lines:
            x = int(self.width/2 + offset * self.width * self.LINE_SPACING)
            line.points = [x, 0, x, self.height]
            offset += 1

class SpaceshipApp(App):
    pass

SpaceshipApp().run()