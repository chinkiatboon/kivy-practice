from kivy.uix.relativelayout import RelativeLayout


def on_touch_down(self, touch):
    if self.game_over == False:
        if touch.x < self.width/2:
            self.move_factor = 1
        else:
            self.move_factor = -1
    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    if self.game_over == False:
        self.move_factor = 0

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if self.game_over == False: 
        if keycode[1] == 'left':
            self.move_factor = 1
        elif keycode[1] == 'right':
            self.move_factor = -1
        return True

def on_keyboard_up(self, keyboard, keycode):
    if self.game_over == False:
        self.move_factor = 0
        return True

def keyboard_closed(self):
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.unbind(on_key_up=self.on_keyboard_up)
    self.keyboard = None