
from kivy.app import App


class AccountCreator:
    def create_account(self, *args):
        return App.get_running_app().server_bridge.signup(*args)


