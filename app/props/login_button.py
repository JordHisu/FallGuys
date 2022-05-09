
from kivy.uix.button import Button
from kivy.app import App


class LoginButton(Button):
    def login(self):
        session_manager = App.get_running_app().session_manager
        session_manager.login()
        App.get_running_app().root.screen_manager.change_screen("BodyStanceScreen")

    def on_release(self):
        self.login()
