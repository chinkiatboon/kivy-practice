from kivy.uix.relativelayout import RelativeLayout

class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:               # if menu is hidden, disable touch on menu
            return False
        return super(RelativeLayout, self).on_touch_down(touch)