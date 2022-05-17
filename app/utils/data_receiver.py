
from utils.data.gps_data import GPSData
from utils.data.barometer_data import BarometerData
from utils.data.step_data import StepData
from utils.data.notification_data import NotificationData
from kivy.clock import Clock
from random import uniform, choice


class DataReceiver:
    data_types = {
        'gps':          {'class': GPSData,          'callbacks': []},
        'barometer':    {'class': BarometerData,    'callbacks': []},
        'step':         {'class': StepData,         'callbacks': []},
        'notification': {'class': NotificationData, 'callbacks': []},
    }

    def __init__(self):
        Clock.schedule_interval(self._generate_fake_data, timeout=5)

    def receive_data(self, data):
        # Server entrypoint for the app
        parsed_data = [self._create_wrapper(data_type, *content) for data_type, content in data]
        for item in parsed_data:
            self._dispatch(item)

    def add_gps_callback(self, callback):
        self.data_types['gps']['callbacks'].append(callback)

    def add_barometer_callback(self, callback):
        self.data_types['barometer']['callbacks'].append(callback)

    def add_step_callback(self, callback):
        self.data_types['step']['callbacks'].append(callback)

    def add_notification_callback(self, callback):
        self.data_types['notification']['callbacks'].append(callback)

    def _generate_fake_data(self, dt):
        data = {
            ('gps', (uniform(-70, 70), uniform(-100, 100))),
            ('barometer', ('anklet',  uniform(0, 50))),
            ('barometer', ('base', uniform(0, 50))),
            ('barometer', ('necklace', uniform(0, 50))),
            ('step', (uniform(10, 50), )),
            ('notification', choice([
                ('fall', 'The user has fallen'),
                ('panic', 'The user pressed the panic button!!'),
                ('stand', ''),
                ('lying', '')
            ]))
        }
        self.receive_data(data)

    def _create_wrapper(self, data_type, *args):
        cls = self.data_types[data_type]['class']
        return cls(data_type, *args)

    def _dispatch(self, item):
        callbacks = self.data_types[item.data_type]['callbacks']
        for callback in callbacks:
            callback(item)




