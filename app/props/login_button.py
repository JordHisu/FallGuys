
from kivy.uix.button import Button
from kivy.app import App


class LoginButton(Button):
    def login(self):
        session_manager = App.get_running_app().session_manager
        session_manager.login()
        App.get_running_app().root.ids.screen_manager.change_screen("HealthScreen")

    def on_release(self):
        self.login()
