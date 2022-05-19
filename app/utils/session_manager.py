
from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class SessionManager(EventDispatcher):
    USER_LOGGED = BooleanProperty(False)
    AUTH_TOKEN = None

    def login(self, email, password):
        app = App.get_running_app()
        auth_code = app.server_bridge.login(email, password)
        if auth_code is None:
            return
        self.AUTH_TOKEN = auth_code
        self.USER_LOGGED = True
        # Probably not the best place to put this
        configs = app.config_manager.get_configs_from_server()
        app.save_configs(configs)

    def logout(self):
        self.USER_LOGGED = False
        self.AUTH_TOKEN = ""
