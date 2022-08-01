import kivy
kivy.require('1.0.1')

from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, Clock
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up, keyboard_closed

    V_NUM_LINES = 6        
    V_LINE_SPACING = 0.1  # Percentage instead of numeric figure

    H_NUM_LINES = 10
    H_LINE_SPACING = 0.1
    VERTICAL_SPEED = 3
    HORIZONTAL_SPEED = 10

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    vertical_lines = []
    horizontal_lines = []

    x_min = 0
    x_max = 0

    current_offset_x = 0
    current_offset_y = 0
    move_factor = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_vertical_lines()
        self.initialize_horizontal_lines()
        
        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down = self.on_keyboard_down)
            self.keyboard.bind(on_key_up = self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def on_size(self, *args):
        print(f'Height: {str(self.height)}, Width: {self.width}')
        self.update_vertical_lines()
        self.update_horizontal_lines()

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

    def get_x_line_coordinates(self, index):
        """
        Function to obtain x coordinates of any vertical line drawn on screen.

        Args:
            index (int): ith vertical line where i = [-n, -n+1, ... n-1, n],
                and total number of lines = 2n + 1  
        """
        true_index = index - 0.5  # remove 0.5 used to center board
        spacing = self.V_LINE_SPACING * self.width
        central_line_x = self.perspective_point_x  # the spaceship shall remain in center

        # Consider a case where index = 0.
        # This line is by default 0.5 spacings to the left of the central line.
        x = central_line_x + true_index * spacing + self.current_offset_x

        return x

    def update_vertical_lines(self):
        offset = -self.V_NUM_LINES/2 + 0.5  # 0.5 to center board
        self.x_min = self.width/2 + offset * self.width * self.V_LINE_SPACING
        self.x_max = self.width/2 - offset * self.width * self.V_LINE_SPACING
        start_index = -int(self.V_NUM_LINES/2) + 1
        end_index = start_index + self.V_NUM_LINES
        
        for i in range(start_index, end_index):
            x = self.get_x_line_coordinates(i)
            x1, y1 = self.transform(x, 0)
            x2, y2 = self.transform(x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        line_count = 0
        for line in self.horizontal_lines:
            line_count += 1
            y = self.H_LINE_SPACING * line_count * self.height - self.current_offset_y
            x1, y1 = self.transform(self.x_min+self.current_offset_x, y)
            x2, y2 = self.transform(self.x_max+self.current_offset_x, y)
            line.points = [x1, y1, x2, y2]

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.VERTICAL_SPEED * dt * 60
        self.current_offset_x += self.move_factor * self.HORIZONTAL_SPEED * dt * 60

        if self.current_offset_y > self.H_LINE_SPACING * self.height:
            self.current_offset_y -= self.H_LINE_SPACING * self.height

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True

class SpaceshipApp(App):
    pass

SpaceshipApp().run()