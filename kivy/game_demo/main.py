import kivy, random
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
from kivy.graphics.vertex_instructions import Line, Quad

class MainWidget(Widget):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up, keyboard_closed

    V_NUM_LINES = 6        
    V_LINE_SPACING = 0.1  # Percentage instead of numeric figure

    H_NUM_LINES = 12
    H_LINE_SPACING = 0.1

    NUM_TILES = 10

    VERTICAL_SPEED = 1
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

    tiles = ListProperty([])
    tile_coordinates = ListProperty([])

    step = 0       # increases whenever a horizontal line is "crossed"
    latest_y = 0   # keeps track of latest y index generated
    latest_x = 0   # keeps track of latest x index generated

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_vertical_lines()
        self.initialize_horizontal_lines()
        self.initialize_tiles()
        self.generate_tile_coordinates()

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

    def initialize_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for _ in range(self.NUM_TILES):
                self.tiles.append(Quad())

    def get_x_line_coordinates(self, index):
        """
        Function to obtain x coordinates of any vertical line drawn on screen.

        Args:
            index (int): ith vertical line where i = [-n+1, -n+2, ... n-1, n],
                and total number of lines = 2n
        """
        true_index = index - 0.5 # minus 0.5 to 'center the board'
        spacing = self.V_LINE_SPACING * self.width
        central_line_x = self.perspective_point_x  # the spaceship shall remain in center

        # Consider a case where index = 0.
        # This line is by default 0.5 spacings to the left of the central line.
        x = central_line_x + true_index * spacing + self.current_offset_x

        return x

    def update_vertical_lines(self):
        start_index = -int(self.V_NUM_LINES/2) + 1
        end_index = start_index + self.V_NUM_LINES

        self.x_min = self.get_x_line_coordinates(start_index)
        self.x_max = self.get_x_line_coordinates(end_index-1)

        for i in range(start_index, end_index):
            x = self.get_x_line_coordinates(i)
            x1, y1 = self.transform(x, 0)
            x2, y2 = self.transform(x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def get_y_line_coordinates(self, index):
        """
        Function to obtain y coordinates of any horizontal line drawn on screen.

        Args:
            index (int): ith vertical line where i = [0, 1, ... n-1, n],
                and total number of lines = n
        """
        spacing = self.H_LINE_SPACING * self.height
        y = index * spacing - self.current_offset_y

        return y

    def update_horizontal_lines(self):
        start_index = 0
        end_index = self.H_NUM_LINES

        for i in range(start_index, end_index):
            y = self.get_y_line_coordinates(i)
            x1, y1 = self.transform(self.x_min+self.current_offset_x, y)
            x2, y2 = self.transform(self.x_max+self.current_offset_x, y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def generate_tile_coordinates(self):
        start_index = -int(self.V_NUM_LINES/2) + 1
        end_index = start_index + self.V_NUM_LINES
        r = random.randint(-1,1)

        for i in range(len(self.tile_coordinates)-1, -1, -1):   # Go from backwards to prevent out of index 
                                                                # after deletion from middle
            if self.tile_coordinates[i][1] < self.step:
                del self.tile_coordinates[i]

        # for i in range(len(self.tile_coordinates), self.NUM_TILES):
        #     self.tile_coordinates.append((0, self.latest_y))
        #     self.latest_y += 1

        for i in range(len(self.tile_coordinates), self.NUM_TILES):
            self.tile_coordinates.append((self.latest_x, self.latest_y))
            print(f'latest coordinates: {(self.latest_x, self.latest_y)}')
            if r == -1 and self.latest_x-1 >= start_index:
                self.latest_x -= 1
                self.tile_coordinates.append((self.latest_x, self.latest_y))
            elif r == 1 and self.latest_x+1 < end_index-1:
                self.latest_x += 1
                self.tile_coordinates.append((self.latest_x, self.latest_y))
            self.latest_y += 1

    def get_tile_coordinates(self, index_x, index_y):
        index_y = index_y - self.step
        x = self.get_x_line_coordinates(index_x)
        y = self.get_y_line_coordinates(index_y)
        return x, y

    def update_tiles(self):
        for i in range(self.NUM_TILES):
            x, y = self.tile_coordinates[i] 
            x_min, y_min = self.get_tile_coordinates(x, y)
            x_max, y_max = self.get_tile_coordinates(x + 1, y + 1)

            x1, y1 = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)

            self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update(self, dt):
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.current_offset_y += self.VERTICAL_SPEED * dt * 60
        self.current_offset_x += self.move_factor * self.HORIZONTAL_SPEED * dt * 60

        if self.current_offset_y > self.H_LINE_SPACING * self.height:
            self.current_offset_y -= self.H_LINE_SPACING * self.height
            self.step += 1
            self.generate_tile_coordinates() # Generate new tiles upon new step

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True

class SpaceshipApp(App):
    pass

SpaceshipApp().run()