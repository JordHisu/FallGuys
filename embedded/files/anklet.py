from files.modules.bluetooth import Bluetooth
from files.modules.barometer import Barometer
from files.utils.logger import Logger
import utime


class Anklet:
    def __init__(self):
        self.log = Logger()
        self.bluetooth = Bluetooth(
            name="Anklet",
            uart_num=0,
            tx_pin=12,
            rx_pin=13,
            is_slave=True,
            log=self.log
        )
        self.barometer = Barometer(
            i2c_num=1,
            scl_pin=3,
            sda_pin=2,
            log=self.log,
            address=0x77
        )

    def run(self):
        while True:
            barometer_data = self.barometer.getBarometerData()
            bluetooth_received = self.bluetooth.receive()
            if bluetooth_received:
                if "ALERT" in bluetooth_received:
                    #send to LoRa alert
                    print("Send to LORA")
                else:
                    try:
                        if int(bluetooth_received) - int(barometer_data) > 1:
                            # send alert to LoRa
                            print("Fall detected")
                    except Exception as e:
                        self.log.error(str(e))

            # get data from GPS
            # get data from Accelerometer
            # send datas to LoRa
            # if received data from LoRa, alter the configuration
            print(barometer_data)
            print(bluetooth_received)
            utime.sleep(1)
