from files.modules.bluetooth import Bluetooth
from files.modules.barometer import Barometer
from files.utils.logger import Logger
import utime

class Necklace:
    def __init__(self):
        self.log = Logger()
        self.bluetooth = Bluetooth(
            name= "Necklace",
            uart_num= 0,
            tx_pin=12,
            rx_pin=13,
            is_slave=True,
            log=self.log
        )
        self.barometer = Barometer(
            i2c_num=0,
            scl_pin=12,
            sda_pin=13,
            log=self.log,
            address=0x77
        )
    
    def run(self):
        while True:
            barometer_data = self.barometer.getBarometerData()
            self.bluetooth.send(barometer_data)
            utime.sleep(1)