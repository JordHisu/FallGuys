
from utils.data.gps_data import GPSData
from kivy.clock import Clock
from random import uniform


class DataReceiver:
    data_types = {
        'gps': {'class': GPSData, 'callback': None}
    }

    def __init__(self):
        Clock.schedule_interval(self._generate_fake_data, timeout=15)

    def receive_data(self, data):
        # Server entrypoint for the app
        received = [self._create_wrapper(name, item) for name, item in data.items()]
        for item in received:
            self._dispatch(item)

    def set_gps_callback(self, callback):
        self.data_types['gps']['callback'] = callback

    def _generate_fake_data(self, dt):
        data = {'gps': (uniform(-70, 70), uniform(-100, 100))}
        self.receive_data(data)

    def _create_wrapper(self, name, content):
        cls = self.data_types[name]['class']
        return cls(name, *content)

    def _dispatch(self, item):
        callback = self.data_types[item.name]['callback']
        if callback is None:
            return
        callback(item)




