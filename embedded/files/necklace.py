from files.modules.bluetooth_uart import Bluetooth
from files.modules.barometer import Barometer
from files.modules.button import Button
from files.utils.logger import Logger
from files.utils.blink_led import toggle_led
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
        self.barometer_data = None

    def get_data_barometer(self, *args):
        data = self.barometer.getAltitude()
        print("Barometer data: " + str(data))
        self.barometer_data = data

    def send_bluetooth(self, *args):
        if self.barometer_data is None:
            return

        self.bluetooth.send(self.barometer_data)
        if self.button.is_changed_state():
            self.bluetooth.send("ALERT")
    
    def run(self):
        previous_bluetooth = utime.ticks_ms()
        previous_barometer = utime.ticks_ms()
        previous_led = utime.ticks_ms()
        while True:
            if utime.ticks_ms() - previous_bluetooth > 5000:
                self.send_bluetooth()
                previous_bluetooth = utime.ticks_ms()
            if utime.ticks_ms() - previous_led > 400:
                toggle_led()
                previous_led = utime.ticks_ms()
            if utime.ticks_ms() - previous_barometer > 2000:
                self.get_data_barometer()
                previous_barometer = utime.ticks_ms()
            # utime.sleep(1)
