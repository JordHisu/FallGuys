from dataclasses import dataclass


@dataclass
class GPSData:
    data_type: str
    lat: float
    lon: float