from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

Builder.load_file("screens/live_location_screen_layout.kv")


class LiveLocationScreen(Screen):
    def receive_gps_data(self, gps_data):
        self.ids.map.center_on(gps_data.lat, gps_data.lon)
        self.ids.marker.lat = gps_data.lat
        self.ids.marker.lon = gps_data.lon


