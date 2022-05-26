from files.modules.accelerometer import Accelerometer
from _thread import start_new_thread
import utime

class Measurements:
    def __init__(self, stepcallback) -> None:
        self.accelerometer = Accelerometer(
            i2c_num=0,
            scl_pin=21,
            sda_pin=20,
            log=None,
            address=0x53,
            irq_callback = self.stepcallback
        )
    
    def _loop(self):
        while True:
            self.accelerometer.stepIteration()
    
    def start(self):
        start_new_thread(self._loop)

if __name__ == "__main__":
    m = Measurements()
    m.start()
    while True:
        print("macarrão batata qualquer coisa")
        utime.sleep(0.5)