
from kivy.uix.floatlayout import FloatLayout


class Footer(FloatLayout):
    def unselect_all_image_buttons(self):
        for image_button in self.ids.navbar.children:
            image_button.unselect()
