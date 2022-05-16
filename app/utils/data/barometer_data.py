

from dataclasses import dataclass


@dataclass
class BarometerData:
    data_type: str
    source: str
    value: float

