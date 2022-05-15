from files.modules.bluetooth import Bluetooth
from files.modules.barometer import Barometer
from files.utils.logger import Logger
import utime


class Anklet:
    def __init__(self):
        self.log = Logger()
        self.bluetooth_necklace = Bluetooth(
            name="Anklet",
            uart_num=0,
            tx_pin=12,
            rx_pin=13,
            is_slave=False,
            log=self.log
        )
        self.barometer = Barometer(
            i2c_num=0,
            scl_pin=3,
            sda_pin=2,
            log=self.log,
            address=0x77
        )

    def run(self):
        while True:
            barometer_data = self.barometer.getBarometerData()
            barometer_bluetooth_received = self.bluetooth_necklace.receive()
            print(barometer_data)
            print(barometer_bluetooth_received)
            utime.sleep(1)