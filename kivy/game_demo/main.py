import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, Clock
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    V_NUM_LINES = 6        
    V_LINE_SPACING = 0.1  # Percentage instead of numeric figure

    H_NUM_LINES = 10
    H_LINE_SPACING = 0.1
    MOVE_SPEED = 1

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    vertical_lines = []
    horizontal_lines = []

    x_min = 0
    x_max = 0

    current_offset_y = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_vertical_lines()
        self.initialize_horizontal_lines()
        Clock.schedule_interval(self.update, 1/60)

    def on_size(self, *args):
        print(f'Height: {str(self.height)}, Width: {self.width}')
        self.update_vertical_lines()
        self.update_horizontal_lines()

    def on_perspective_point_x(self, widget, value):
        pass

    def on_perspective_point_y(self, widget, value):
        pass

    def initialize_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.V_NUM_LINES):
                self.vertical_lines.append(Line())

    def initialize_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.H_NUM_LINES):
                self.horizontal_lines.append(Line())

    def update_vertical_lines(self):
        offset = -int(self.V_NUM_LINES/2) + 0.5  # 0.5 to center board
        self.x_min = int(self.width/2 + offset * self.width * self.V_LINE_SPACING)
        self.x_max = int(self.width/2 - offset * self.width * self.V_LINE_SPACING)

        for line in self.vertical_lines:
            x = int(self.width/2 + offset * self.width * self.V_LINE_SPACING)
            x1, y1 = self.transform(x, 0)
            x2, y2 = self.transform(x, self.height)
            line.points = [x1, y1, x2, y2]
            offset += 1

    def update_horizontal_lines(self):
        line_count = 0
        for line in self.horizontal_lines:
            line_count += 1
            y = self.H_LINE_SPACING * line_count * self.height - self.current_offset_y
            x1, y1 = self.transform(self.x_min, y)
            x2, y2 = self.transform(self.x_max, y)
            line.points = [x1, y1, x2, y2]


    def transform(self, x, y):
        # return self.transform_2D(x,y)
        return self.transform_perspective(x,y)

    def transform_2D(self, x, y):
        """
        To be used if we want to see the game board from the top (2D).
        For debugging purposes.
        """
        return int(x), int(y)

    def transform_perspective(self, x, y):
        """
        Transforms (x,y) coordinates to give a more 3D feel.
        """
        # Calculate new y based on proportion 
        y = y / self.height * self.perspective_point_y
        if y > self.perspective_point_y:
            y = self.perspective_point_y

        # Calculate new x. We can visually note that new x is dependent on y.
        x_diff = x - self.perspective_point_x  
        y_factor = ((self.perspective_point_y - y )/self.perspective_point_y)**2    # Squared to account for proportion of 
                                                                                    # horizontal lines

        x = self.perspective_point_x + x_diff * y_factor                            # Recalculate x based on 
                                                                                    # proportion of y 

        y = self.perspective_point_y - y_factor * self.perspective_point_y

        return int(x), int(y)

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.MOVE_SPEED

        if self.current_offset_y > self.H_LINE_SPACING * self.height:
            self.current_offset_y -= self.H_LINE_SPACING * self.height

class SpaceshipApp(App):
    pass

SpaceshipApp().run()