
from kivy.uix.button import Button
from kivy.app import App


class CreateAccountButton(Button):
    def create_account(self):
        account_creator = App.get_running_app().account_creator
        account_creator.create_account(**self.creation_arguments)

    def on_release(self):
        self.create_account()
