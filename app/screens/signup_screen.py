from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file("screens/signup_screen_layout.kv")


class SignupScreen(Screen):
    def signup(self):
        account_creator = App.get_running_app().account_creator
        success = account_creator.create_account(
            self.ids.username_input.text,
            self.ids.password_input.text,
            self.ids.email_input.text,
            self.ids.phone_input.text,
            self.ids.device_id_input.text,
        )

        if not success:
            return

        App.get_running_app().root.ids.screen_manager.change_screen("LoginScreen")
