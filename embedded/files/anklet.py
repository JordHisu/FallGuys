# from files.modules.bluetooth_uart import Bluetooth
from files.modules.bluetooth_i2c import Bluetooth
from files.modules.barometer import Barometer
from files.modules.lora import LoRa
from files.modules.gps import GPS
from files.utils.logger import Logger
from files.utils.blink_led import toggle_led
import utime
import re


class Anklet:
    def __init__(self):
        self.log = Logger()
        self.bluetooth = Bluetooth(
            i2c_num=0,
            scl_pin=13,
            sda_pin=12,
            log=self.log
        )
        self.barometer = Barometer(
            i2c_num=1,
            scl_pin=3,
            sda_pin=2,
            log=self.log,
            address=0x77
        )
        self.lora = LoRa(
            uart_num=0,
            tx_pin=0,
            rx_pin=1,
            m0=6,
            m1=7,
            log=self.log
        )
        self.gps = GPS(
            uart_num=1,
            tx_pin=8,
            rx_pin=9,
            enable_pin=26
        )

        self.bar_pooling = 30
        self.bar_mills = utime.ticks_ms()
        
        self.gps_pooling = 300
        self.gps_mills = utime.ticks_ms()

        self.first_time = True
        self.offset = 0


    def run(self):
        self.lora.send('Anklet is running')
        print('Anklet is running')
        while True:
            try:
                self.loop()
            except Exception as e:
                print('Error: ', str(e))
            utime.sleep(0.3)

    def loop(self):
        toggle_led()
        self.receive_bluetooth()
        self.get_gps()

    def receive_bluetooth(self):
        bluetooth_received = self.bluetooth.receive()
        if not bluetooth_received:
            return

        if "ALERT" in bluetooth_received:
            self.lora.send({'type': 'BUT'})

        parsed_bluetooth = self.parse_bluetooth(bluetooth_received)
        if not parsed_bluetooth:
            return

        barometer_data = float(self.barometer.getAltitude())
        if self.first_time:
            self.offset = parsed_bluetooth - barometer_data
            self.first_time = False

        bar_data = self.build_barometer_data(parsed_bluetooth, barometer_data)
        if parsed_bluetooth - barometer_data < 0.4:
            bar_data['fall'] = True
            self.log.info("FALL DETECTED: Send to LoRa")
            self.lora.send(bar_data)
        elif utime.ticks_ms() - self.bar_mills > self.bar_pooling * 1000:
            self.lora.send(bar_data)
            self.bar_mills = utime.ticks_ms()

    def build_barometer_data(self, parsed_bt, barometer_data):
        return {
            'type': 'BAR',
            'necklace': parsed_bt,
            'anklet': barometer_data,
            'fall': False
        }

    def parse_bluetooth(self, bt_msg):
        regx = re.search("(\d+(.\d+)?)", bt_msg)
        if not regx:
            return False

        regx = regx.groups()
        if not regx:
            return False

        return float(regx[0]) - self.offset

    def get_gps(self):
        if not utime.ticks_ms() - self.gps_mills > self.gps_pooling * 1000:
            return

        print('GETTING GPS INFO')
        lat, lon = self.gps.get_lat_lon()
        gps_data = {
            "type": "GPS",
            "lat": lat,
            "lon": lon
        }
        # print(gps_data)
        self.lora.send(gps_data)
        self.gps_mills = utime.ticks_ms()