
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class SessionManager(EventDispatcher):
    USER_LOGGED = BooleanProperty(False)

    def login(self):
        self.USER_LOGGED = True

    def logout(self):
        self.USER_LOGGED = False
