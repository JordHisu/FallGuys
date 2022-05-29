# from files.modules.bluetooth_uart import Bluetooth
from files.modules.bluetooth_i2c import Bluetooth
from files.modules.barometer import Barometer
from files.modules.lora import LoRa
from files.modules.accelerometer import Accelerometer
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
        # self.accelerometer = Accelerometer(
        #     i2c_num=0,
        #     scl_pin=21,
        #     sda_pin=20,
        #     log=self.log,
        #     address=0x53
        # )

        self.bar_pooling = 10
        self.bar_mills = utime.ticks_ms()

        self.first_time = True
        self.offset = 0


    def run(self):
        self.lora.send('Anklet running\n')
        while True:
            try:
                toggle_led()
                barometer_data = self.barometer.getBarometerData()
                bluetooth_received = self.bluetooth.receive()
                if bluetooth_received:
                    regx = re.search("(\d+(.\d+)?)", bluetooth_received)
                    if "ALERT" in bluetooth_received:
                        self.lora.send({'type': 'BUT'})
                    if regx:
                        regx = regx.groups()
                        if regx:
                            bluetooth_received = float(regx[0]) - self.offset
                            barometer_data = float(barometer_data)
                            if self.first_time:
                                self.offset =  bluetooth_received - barometer_data
                                self.first_time = False
                            bar_data = {
                                'type': 'BAR',
                                'necklace': bluetooth_received,
                                'anklet': barometer_data,
                                'fall': False
                            }
                            if barometer_data - bluetooth_received < 0.4:
                                bar_data['fall'] = True
                                self.log.info("FALL DETECTED: Send to LoRa")
                                self.lora.send(bar_data)
                            else:
                                if utime.ticks_ms() - self.bar_mills > self.bar_pooling * 1000:
                                    self.lora.send(bar_data)
                                    self.bar_mills = utime.ticks_ms()
            except Exception as e:
                print('Error: ', str(e))

            utime.sleep(0.5)
