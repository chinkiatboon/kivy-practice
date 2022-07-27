import kivy
kivy.require('1.0.1')

from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout

class WidgetsExample(GridLayout):
    my_text = StringProperty("0")
    slider_value = StringProperty("70")
    count = 0
    count_color = ListProperty([1,1,1,1])
    slider_color = ListProperty([1,0.5,0.5,1])
    enable_count = BooleanProperty(False)

    def on_button_click(self):
        if self.enable_count == True:
            self.count = self.count + 1
            self.my_text = str(self.count)
            if self.count%10 == 0 and self.count != 0:
                self.count_color = [0.75,0,0,1]
            else:
                self.count_color = [1,1,0,1]

    def on_toggle_button_state(self, toggle):
        if toggle.state == 'down':
            toggle.text = 'ON'
            self.enable_count = True
        else:
            toggle.text = 'OFF'
            self.enable_count = False

    def on_slider_value(self, slider):
        self.slider_color = [1,(100-int(slider.value))/100,(100-int(slider.value))/100,1]


class TheLabApp(App):
    pass

TheLabApp().run()
