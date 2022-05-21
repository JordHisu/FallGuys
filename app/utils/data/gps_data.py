from dataclasses import dataclass


@dataclass
class GPSData:
    data_type: str
    lat: float
    lon: float

    def __post_init__(self):
        self.filter_lat()
        self.filter_lon()

    def filter_lat(self):
        if self.lat >= 90:
            self.lat = 89.9
        elif self.lat <= -90:
            self.lat = -89.9

    def filter_lon(self):
        if self.lon >= 180:
            self.lon = 179.9
        elif self.lon <= -180:
            self.lon = -179.9


