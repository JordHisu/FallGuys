import os

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from glob import glob


class FallGuysApp(App):
    MAIN_LAYOUT_FILE = 'layout.kv'

    def build(self):
        root = self.load_kv_files()
        return root

    def load_kv_files(self):
        main_path = os.path.dirname(os.path.realpath(__file__))
        layout_files = glob(f"{main_path}/**/*.kv", recursive=True)
        layout_files.remove(f"{main_path}\\{self.MAIN_LAYOUT_FILE}")
        for file in layout_files:
            Builder.load_file(file)
        return Builder.load_file(self.MAIN_LAYOUT_FILE)


class TopOfEverything(FloatLayout):
    INITIAL_WINDOW_SIZE = [300, 533]

    def __init__(self, **kwargs):
        super(TopOfEverything, self).__init__(**kwargs)
        Window.size = self.INITIAL_WINDOW_SIZE
        self.screen_manager = None

    def on_children(self, obj, children):
        new_child = children[0]  # The first element from children is always the new child
        if isinstance(new_child, ScreenManager):
            self.screen_manager = new_child


class MyScreenManager(ScreenManager):
    def add_widget(self, screen, *args, **kwargs):
        super().add_widget(screen, *args, **kwargs)
        screen.root_widget = self.parent

    def change_screen(self, screen_name, *args):
        self.current = screen_name


if __name__ == '__main__':
    FallGuysApp().run()
