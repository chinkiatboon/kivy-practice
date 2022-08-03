import kivy, random
kivy.require('1.0.1')

from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, Clock, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_touch_down, on_touch_up, on_keyboard_down, on_keyboard_up, keyboard_closed

    SHIP_WIDTH = 0.1      # Percentage instead of numeric figure (Percentage of screen width)
    SHIP_HEIGHT = 0.035
    SHIP_FWD = 0.04       # Distance from end of screen to ship (Percentage of screen height)

    V_NUM_LINES = 6      
    V_LINE_SPACING = 0.3  

    H_NUM_LINES = 12
    H_LINE_SPACING = 0.15

    NUM_TILES = 12

    VERTICAL_SPEED = 1
    HORIZONTAL_SPEED = 1.5

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    title_text = StringProperty("SPACESHIP")
    button_text = StringProperty("Start Game")

    vertical_lines = []
    horizontal_lines = []

    x_min = 0
    x_max = 0

    current_offset_x = 0
    current_offset_y = 0
    move_factor = 0

    tiles = ListProperty([])
    tile_coordinates = ListProperty([])

    ship_coordinates = ListProperty([])

    step = 0       # increases whenever a horizontal line is "crossed"
    latest_y = 0   # keeps track of latest y index generated
    latest_x = 0   # keeps track of latest x index generated

    game_over = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_vertical_lines()
        self.initialize_horizontal_lines()
        self.initialize_tiles()
        self.initialize_ship()
        self.generate_tile_coordinates()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down = self.on_keyboard_down)
            self.keyboard.bind(on_key_up = self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def initialize(self):
        self.current_offset_x = 0
        self.current_offset_y = 0
        self.move_factor = 0
        self.step = 0       # increases whenever a horizontal line is "crossed"
        self.latest_y = 0   # keeps track of latest y index generated
        self.latest_x = 0   # keeps track of latest x index generated

        self.tile_coordinates = []
        self.generate_tile_coordinates()

        self.game_over = False

    def start_game(self):
        print(f"click")
        self.game_over = False
        self.initialize()
        self.menu_widget.opacity = 0

    def game_over_display(self):
        self.title_text = "Game over!"
        self.button_text = "Restart"
        self.menu_widget.opacity = 1

    def on_size(self, *args):
        print(f'Height: {str(self.height)}, Width: {self.width}')
        self.update_vertical_lines()
        self.update_horizontal_lines()

    def initialize_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()
            for i in range(3):
                self.ship_coordinates.append((0,0))

    def update_ship(self):
        x_mid = self.perspective_point_x
        x_left = x_mid - self.SHIP_WIDTH * self.width / 2
        x_right = x_mid + self.SHIP_WIDTH * self.width / 2 

        y_top = (self.SHIP_HEIGHT + self.SHIP_FWD) * self.height
        y_bottom = self.SHIP_FWD * self.height

        self.ship_coordinates[0] = (x_left,y_bottom)
        self.ship_coordinates[1] = (x_mid, y_top)
        self.ship_coordinates[2] = (x_right, y_bottom)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

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
            x1, y1 = self.transform(self.x_min, y)
            x2, y2 = self.transform(self.x_max, y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def generate_tile_coordinates(self):
        start_index = -int(self.V_NUM_LINES/2) + 1
        end_index = start_index + self.V_NUM_LINES
        r = random.randint(-1,1)

        for i in range(len(self.tile_coordinates)-1, -1, -1):   # Go from backwards to prevent out of index 
                                                                # after deletion from middle
            if self.tile_coordinates[i][1] < self.step:
                del self.tile_coordinates[i]

        for i in range(len(self.tile_coordinates), self.NUM_TILES):
            if self.step <= self.NUM_TILES:
                self.tile_coordinates.append((0, self.latest_y))
            else:
                self.tile_coordinates.append((self.latest_x, self.latest_y))
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

    def check_on_path(self): 
        left_on_path = False
        top_on_path = False
        right_on_path = False

        for i in range(self.NUM_TILES):
            if self.tile_coordinates[i][1] < self.step + 2:  # tiles too far away arent useful in checking for collision
                x, y = self.tile_coordinates[i]
                x_min, y_min = self.get_tile_coordinates(x,y)
                x_max, y_max = self.get_tile_coordinates(x+1, y+1)

                if x_min <= self.ship_coordinates[0][0] <= x_max and y_min <= self.ship_coordinates[0][1] <= y_max:  # if left point on path
                    left_on_path = True
                if x_min <= self.ship_coordinates[1][0] <= x_max and y_min <= self.ship_coordinates[1][1] <= y_max:  # if top point on path
                    top_on_path = True
                if x_min <= self.ship_coordinates[2][0] <= x_max and y_min <= self.ship_coordinates[2][1] <= y_max:  # if right point on path
                    right_on_path = True
                
        if False in [left_on_path,top_on_path,right_on_path]:
            self.game_over_display()
            return False
        else:
            return True

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
        self.update_ship()
        if self.game_over is False and self.check_on_path() is False:
            self.game_over = True

        if self.game_over is False:
            self.current_offset_y += self.VERTICAL_SPEED * dt * 60 * self.height / 200
            self.current_offset_x += self.move_factor * self.HORIZONTAL_SPEED * dt * 60 * self.width / 200
            while self.current_offset_y > self.H_LINE_SPACING * self.height:
                self.current_offset_y -= self.H_LINE_SPACING * self.height
                self.step += 1
                self.generate_tile_coordinates() # Generate new tiles upon new step

    def is_desktop(self):
        if platform in ('linux', 'win', 'macosx'):
            return True

class SpaceshipApp(App):
    pass

SpaceshipApp().run()