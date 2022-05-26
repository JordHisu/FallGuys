# from files.modules.bluetooth_uart import Bluetooth
from files.modules.bluetooth_i2c import Bluetooth
from files.modules.barometer import Barometer
from files.modules.lora import LoRa
from files.modules.accelerometer import Accelerometer
from files.utils.logger import Logger
import utime


class Anklet:
    def __init__(self):
        self.log = Logger()
        # self.bluetooth = Bluetooth(
        #     name="Anklet",
        #     uart_num=0,
        #     tx_pin=12,
        #     rx_pin=13,
        #     is_slave=True,
        #     log=self.log
        # )
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

        self.gps_pooling = 120
        self.acc_pooling = 60
        self.bar_pooling = 30

        self.gps_mills, self.acc_mills, self.bar_mills = utime.ticks_ms()

    def run(self):
        while True:
            barometer_data = self.barometer.getBarometerData()
            bluetooth_received = self.bluetooth.receive()
            if bluetooth_received:
                if "CONNECTED" in bluetooth_received:
                    print("Connected Bluetooth")
                    self.log.info("Connected Bluetooth")
                elif "ALERT" in bluetooth_received:
                    print("BUTTON ALERT: Send to LoRa")
                    self.log.info("BUTTON ALERT: Send to LoRa")
                    self.lora.send({'type': 'BUT'})
                else:
                    try:
                        barometer_data = float(barometer_data) - 0.675  # offset to equal the barometers
                        bluetooth_received = float(bluetooth_received)
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
                            if (utime.ticks_ms() - self.bar_mills) > self.bar_pooling * 1000:
                                self.lora.send(bar_data)
                                self.bar_mills = utime.ticks_ms()

                    except Exception as e:
                        self.log.error("Converting Bluetooth or Barometer Data " + str(e))

            if (utime.ticks_ms() - self.gps_mills) > self.gps_pooling * 1000:
                # get data from GPS
                gps_data = {
                    'type': 'GPS',
                    'lat': -25.4395054,
                    'lon': -49.2685292
                }
                self.lora.send(gps_data)
                self.gps_mills = utime.ticks_ms()

            # get data from Accelerometer
            if (utime.ticks_ms() - self.acc_mills) > self.acc_pooling * 1000:
                acc_data = {
                    'type': 'ACC',
                    'steps': 35,
                }
                self.lora.send(acc_data)
                self.acc_mills = utime.ticks_ms()

            # lora_rcv = self.lora.receive()
            # if lora_rcv:
            #     print('Received message from LoRa: ' + str(lora_rcv))
            utime.sleep(0.5)
