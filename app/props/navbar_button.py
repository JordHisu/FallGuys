from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

Builder.load_file("props/navbar_button_layout.kv")


class NavbarButton(ButtonBehavior, Image):
    def toggle(self):
        self.source = self.unselected_image if self.selected else self.selected_image
        self.selected = not self.selected

    def unselect(self):
        self.source = self.unselected_image
        self.selected = False

    def select(self):
        self.source = self.selected_image
        self.selected = True
