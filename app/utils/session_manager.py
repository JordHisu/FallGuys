
from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class SessionManager(EventDispatcher):
    USER_LOGGED = BooleanProperty(False)
    AUTH_TOKEN = None

    def login(self, email, password):
        auth_code = App.get_running_app().server_bridge.login(email, password)
        if auth_code is None:
            return
        self.AUTH_TOKEN = auth_code
        self.USER_LOGGED = True

    def logout(self):
        self.USER_LOGGED = False
        self.AUTH_TOKEN = ""
