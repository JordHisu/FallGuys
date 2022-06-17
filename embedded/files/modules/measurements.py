import gc
from files.modules.accelerometer import Accelerometer
from _thread import start_new_thread
import utime


class Measurements:
    def __init__(self, stepcallback, i2c) -> None:
        self.accelerometer = Accelerometer(
            i2c=i2c,
            log=None,
            address=0x53,
            irq_callback=stepcallback
        )
    
    def _loop(self):
        i = 0
        while True:
            i += 1
            if i % 25 is 0:
                gc.collect()
            self.accelerometer.stepIteration()
    
    def start(self):
        start_new_thread(self._loop, ())

if __name__ == "__main__":
    m = Measurements()
    m.start()
    while True:
        print("macarrão batata qualquer coisa")
        utime.sleep(0.5)