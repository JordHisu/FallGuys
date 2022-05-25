from files.modules.bluetooth_uart import Bluetooth
from files.modules.barometer import Barometer
from files.modules.button import Button
from files.utils.logger import Logger
import utime

class Necklace:
    def __init__(self):
        self.log = Logger()
        self.bluetooth = Bluetooth(
            name="Necklace",
            uart_num=0,
            tx_pin=12,
            rx_pin=13,
            is_slave=False,
            log=self.log
        )
        self.barometer = Barometer(
            i2c_num=1,
            scl_pin=3,
            sda_pin=2,
            log=self.log,
            address=0x77
        )
        self.button = Button(
            pin=14, log=self.log
        )
    
    def run(self):
        while True:
            barometer_data = self.barometer.getBarometerData()
            self.bluetooth.send(barometer_data)
            if self.button.is_changed_state():
                self.bluetooth.send("ALERT")
            utime.sleep(0.5)
