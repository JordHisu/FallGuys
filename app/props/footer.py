from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation

Builder.load_file("props/footer_layout.kv")


class Footer(FloatLayout):
    def unselect_all_image_buttons(self):
        for image_button in self.ids.navbar.children:
            image_button.unselect()

    def select_button(self, navbar_button_destination):
        self.unselect_all_image_buttons()
        for child in self.ids.navbar.children:
            if child.destination == navbar_button_destination:
                child.select()
                break

    def hide(self):
        Animation(size_hint_y=0, duration=.2).start(self)

    def show(self):
        Animation(size_hint_y=self.true_size_hint_y, duration=.2).start(self)
