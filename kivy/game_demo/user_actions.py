def on_touch_down(self, touch):
    if touch.x < self.width/2:
        self.move_factor = 1
    else:
        self.move_factor = -1

def on_touch_up(self, touch):
    self.move_factor = 0

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.move_factor = 1
    elif keycode[1] == 'right':
        self.move_factor = -1
    return True

def on_keyboard_up(self, keyboard, keycode):
    self.move_factor = 0
    return True

def keyboard_closed(self):
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.unbind(on_key_up=self.on_keyboard_up)
    self.keyboard = None