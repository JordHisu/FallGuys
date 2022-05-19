
from kivy.app import App


class ConfigManager:
    def send_config_to_server(self, config_name, value):
        App.get_running_app().server_bridge.send_config(config_name, value)

    def get_configs_from_server(self):
        return App.get_running_app().server_bridge.get_configs()
