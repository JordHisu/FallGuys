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
                if "CONNECTED" in bluetooth_received:
                    print("Connected Bluetooth")
                    self.log.info("Connected Bluetooth")
                elif "ALERT" in bluetooth_received:
                    #send to LoRa alert
                    print("BUTTON ALERT: Send to LoRa")
                else:
                    try:
                        barometer_data = float(barometer_data) - 0.675  # offset to equal the barometers
                        bluetooth_received = float(bluetooth_received)
                        if barometer_data - bluetooth_received < 0.4:
                            # send alert to LoRa
                            print("Fall detected - Send to LoRa")
                    except Exception as e:
                        print("Error")
                        self.log.error("Converting Bluetooth or Barometer Data " + str(e))

            # get data from GPS
            # get data from Accelerometer
            # send datas to LoRa
            # if received data from LoRa, alter the configuration
            utime.sleep(1)
