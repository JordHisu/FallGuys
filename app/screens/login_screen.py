from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("screens/login_screen_layout.kv")


class LoginScreen(Screen):
    def login(self):
        email = self.ids.username_input.text
        password = self.ids.password_input.text

        app = App.get_running_app()
        session_manager = app.session_manager
        session_manager.login(email, password)

        if session_manager.USER_LOGGED:
            app.server_bridge.get_last_day_data()
            App.get_running_app().root.ids.screen_manager.change_screen("HealthScreen")


