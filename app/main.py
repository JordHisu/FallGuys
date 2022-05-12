import json
import os
from pathlib import Path

import kivy.utils
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.settings import SettingsWithNoMenu

from utils.account_creator import AccountCreator
from utils.config_manager import ConfigManager
from utils.notification_handler import NotificationHandler
from utils.session_manager import SessionManager
from utils.data_receiver import DataReceiver


class FallGuysApp(App):
    MAIN_LAYOUT_FILE = 'layout.kv'
    session_manager = SessionManager()
    account_creator = AccountCreator()
    notification_handler = NotificationHandler()
    config_manager = ConfigManager()
    data_receiver = DataReceiver()

    def build(self):
        self.settings_cls = SettingsWithNoMenu
        self.use_kivy_settings = False
        return Builder.load_file(self.MAIN_LAYOUT_FILE)

    def on_start(self):
        settings = self.create_settings()
        settings_screen = self.root.ids.screen_manager.get_screen("SettingsScreen")
        settings_screen.ids.settings_box.add_widget(settings)

        stored_notifications = json.loads(self.config.get('storage', 'notifications'))
        for notification in stored_notifications:
            self.root.ids.screen_manager.get_screen("NotificationScreen").add_notification(notification)

        gps_callback = self.root.ids.screen_manager.get_screen("LiveLocationScreen").receive_gps_data
        self.data_receiver.set_gps_callback(gps_callback)

    def on_stop(self):
        notifications = self.root.ids.screen_manager.get_screen("NotificationScreen").get_current_notifications_json()
        self.config.set('storage', 'notifications', json.dumps(notifications))
        self.config.write()

    def build_config(self, config):
        target_path = self.resolve_path("utils/default_configuration.json")
        with open(target_path, 'r') as config_file:
            config_json = json.load(config_file)
        for title, content in config_json.items():
            config.setdefaults(title, content)

    def build_settings(self, settings):
        target_path = self.resolve_path("utils/editable_settings.json")
        settings.add_json_panel('', self.config, filename=target_path)

    def on_config_change(self, config, section, key, value):
        self.config_manager.send_config_to_server(key, value)

    def resolve_path(self, relative_path):
        current_path = Path(os.path.abspath(__file__)).parent.resolve()
        absolute_path = os.path.join(current_path, relative_path)
        return absolute_path


class TopOfEverything(FloatLayout):
    INITIAL_WINDOW_SIZE = [300, 533]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.decide_screen_size()

    def decide_screen_size(self):
        platform = kivy.utils.platform
        if platform == 'win':
            Window.size = self.INITIAL_WINDOW_SIZE


class MyScreenManager(ScreenManager):
    def change_screen(self, screen_name, *args):
        self.parent.ids.footer.select_button(screen_name)
        self.current = screen_name


if __name__ == '__main__':
    FallGuysApp().run()
