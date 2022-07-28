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
            x1, y1 = self.transform(x, 0)
            x2, y2 = self.transform(x, self.height)
            line.points = [x1, y1, x2, y2]
            offset += 1

    def transform(self, x, y):
        # return self.transform_2D(x,y)
        return self.transform_perspective(x,y)

    def transform_2D(self, x, y):
        """
        To be used if we want to see the game board from the top (2D).
        For debugging purposes.
        """
        return x, y

    def transform_perspective(self, x, y):
        """
        Transforms (x,y) coordinates to give a more 3D feel.
        """
        # Calculate new y based on proportion 
        y = y / self.height * self.perspective_point_y

        # Calculate new x. We can visually note that new x is dependent on y.
        x_diff = x - self.perspective_point_x  
        y_factor = (self.perspective_point_y - y )/self.perspective_point_y
        x = self.perspective_point_x + x_diff * y_factor  # Recalculate x based on 
                                                          # proportion of y 

        return x, y

class SpaceshipApp(App):
    pass

SpaceshipApp().run()