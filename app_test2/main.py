import json
import os
from glob import glob
from json import JSONDecodeError

import kivy.utils
import requests
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager


from kivy.uix.relativelayout import RelativeLayout
from datetime import datetime, timedelta
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class FallGuysApp(App):
    MAIN_LAYOUT_FILE = 'layout.kv'

    def build(self):
        root = self.load_kv_files()
        return root

    def load_kv_files(self):
        return Builder.load_file('layout.kv')


class TopOfEverything(FloatLayout):
    INITIAL_WINDOW_SIZE = [300, 533]

    def __init__(self, **kwargs):
        super(TopOfEverything, self).__init__(**kwargs)
        self.decide_screen_size()
        self.screen_manager = None

    def decide_screen_size(self):
        platform = kivy.utils.platform
        if platform == 'win':
            Window.size = self.INITIAL_WINDOW_SIZE


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.after_init, 0)

    def after_init(self, dt):
        App.get_running_app().root.screen_manager = self

    def change_screen(self, screen_name, *args):
        self.current = screen_name


class MainScreen(Screen):
    def make_send_data_request(self):
        url = f"http://fall-guys-integration-workship.herokuapp.com/senddata/{self.get_device_id()}"
        request_body = self._build_json_body_for_send_data_request()
        self.set_terminal_request(request_body)
        response = requests.request(method='post', url=url,
                                    data=json.dumps(request_body),
                                    headers={'content-type': 'application/json'})
        self.set_terminal_response(response.text)

    def _build_json_body_for_send_data_request(self):
        inputs = self.ids.request_options.send_data_request_inputs
        request_body = {}
        for key, (request_input, should_include) in inputs.items():
            if not should_include:
                continue
            try:
                json.loads(request_input)  # If json is valid
                try:
                    eval_input = eval(request_input)
                    if isinstance(eval_input, (list, tuple)):  # If is a list or a tuple
                        for i, item in enumerate(eval_input):
                            eval_input[i] = float(item)
                        request_input = list(eval_input)
                    else:  # If not a list or a tuple, must be a single value
                        request_input = [float(request_input)]
                    request_body[key] = request_input
                except SyntaxError:
                    continue

            except JSONDecodeError:  # If json not valid, try to create from spaced string
                spaced_string_json = self._create_json_from_spaced_string(request_input)
                if spaced_string_json is not None:
                    request_body[key] = eval(spaced_string_json)

        return request_body

    def _create_json_from_spaced_string(self, string):
        splitted_string = string.split(' ')
        for i, substring in enumerate(splitted_string):
            try:
                if (float(substring) and '.' in substring) or substring.isdigit():
                    splitted_string[i] = float(substring)
            except ValueError:
                return None
        try:
            json_from_spaced_string = json.dumps(splitted_string)
        except ValueError:
            json_from_spaced_string = None

        return json_from_spaced_string

    def make_send_notification_request(self, notification_type):
        url = f"http://fall-guys-integration-workship.herokuapp.com/sendnotif/{self.get_device_id()}"
        request_body = {"type": notification_type}
        self.set_terminal_request(request_body)
        response = requests.post(url=url,
                                    data=json.dumps(request_body),
                                    headers={'content-type': 'application/json'})
        self.set_terminal_response(response.text)

    def set_terminal_request(self, text):
        text = json.dumps(text, indent=4)
        self.ids.terminal.ids.request_label.text = str(text)

    def set_terminal_response(self, text):
        try:
            json.loads(text)
            text = json.dumps(text, indent=1)
        except ValueError:
            pass

        self.ids.terminal.ids.response_label.text = text

    def get_device_id(self):
        return self.ids.request_options.ids.device_id_input.text


if __name__ == '__main__':
    FallGuysApp().run()
