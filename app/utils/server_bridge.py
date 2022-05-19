
import requests
from enum import Enum
import json

from kivy.app import App
from kivy.clock import Clock


class Endpoints(Enum):
    LOGIN = "https://fallguys.azurewebsites.net/login"
    SIGNUP = "https://fallguys.azurewebsites.net/createuser"
    GET_NEW_DATA = "https://fallguys.azurewebsites.net/getnewdata"
    GET_LAST_DAY_DATA = "https://fallguys.azurewebsites.net/getlastdaydata"
    GET_CONFIG = "https://fallguys.azurewebsites.net/getconfig"
    SET_CONFIG = "https://fallguys.azurewebsites.net/sendconfig"


class ResponseStatus(Enum):
    OK = "OK"
    ERROR = "ER"


class ServerBridge:
    session_token = ""
    server_request_period = 5
    server_request_event = None

    def set_server_request_period(self, period):
        self.server_request_period = period
        if self.server_request_event is not None:
            self.server_request_event.cancel()
        self.server_request_event = Clock.schedule_interval(lambda dt: self._proxy_caller(self.get_new_data),
                                                            timeout=period)

    def _proxy_caller(self, f, *args, **kwargs):
        if self.session_token in ("", None):
            return
        f(*args, **kwargs)

    def get_new_data(self):
        response = requests.request(method='get', url=Endpoints.GET_NEW_DATA.value,
                                    data=json.dumps(self.session_token), headers={'content-type': 'application/json'})
        data = json.loads(response.text)
        if data["status"] == ResponseStatus.OK.value:
            App.get_running_app().data_receiver.receive_data(data["content"])

    def get_last_day_data(self):
        response = requests.request(method='get', url=Endpoints.GET_LAST_DAY_DATA.value,
                                    data=json.dumps(self.session_token), headers={'content-type': 'application/json'})
        data = json.loads(response.text)
        if data["status"] == ResponseStatus.OK.value:
            App.get_running_app().data_receiver.receive_data(data["content"])

    def login(self, email, password):
        response = requests.request(method='post', url=Endpoints.LOGIN.value,
                                    json={'email': email, 'password': password})
        response_dict = json.loads(response.text)
        if response_dict["status"] != ResponseStatus.OK.value:
            return None
        self.session_token = response_dict["token"]
        return self.session_token

    def signup(self, name, password, email, phone, device):
        credentials = {
            "fullname": name,
            "password": password,
            "email": email,
            "phone": phone,
            "device": device
        }

        response = requests.request(method='post', url=Endpoints.SIGNUP.value, json=credentials)
        response_dict = json.loads(response.text)
        if response_dict["status"] == ResponseStatus.OK.value:
            return True
        return False

    def send_config(self, key, value):
        requests.request(method='post', url=Endpoints.SET_CONFIG.value,
                         json={'config': key, 'value': value, 'token': self.session_token})

    def get_configs(self):
        response = requests.request(method='get', url=Endpoints.GET_CONFIG.value,
                                    data=json.dumps(self.session_token), headers={'content-type': 'application/json'})
        response_dict = json.loads(response.text)
        if response_dict["status"] != ResponseStatus.OK.value:
            return None
        content = {key: value for key, value in response_dict["content"] if value not in ('', None)}
        for key, item in content.items():
            try:
                content[key] = int(float(item))
            except ValueError:
                pass
        return content
