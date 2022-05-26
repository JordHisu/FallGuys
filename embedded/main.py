from time import sleep
from files.modules.accelerometer import Accelerometer
from files.modules.measurements import Measurements
from files.utils.logger import Logger


def run():
    measurements = Measurements(stepcallback)
    measurements.start()

def stepcallback():
    pass

if __name__ == "__main__":
    run()