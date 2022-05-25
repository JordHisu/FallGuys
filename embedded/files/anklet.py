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
            log=self.log
        )
        # self.accelerometer = Accelerometer(
        #     i2c_num=0,
        #     scl_pin=21,
        #     sda_pin=20,
        #     log=self.log,
        #     address=0x53
        # )

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
                    self.lora.send("B")
                else:
                    try:
                        barometer_data = float(barometer_data) - 0.675  # offset to equal the barometers
                        bluetooth_received = float(bluetooth_received)
                        if barometer_data - bluetooth_received < 0.4:
                            print("FALL DETECTED: Send to LoRa")
                            self.log.info("FALL DETECTED: Send to LoRa")
                            self.lora.send("F")
                    except Exception as e:
                        self.log.error("Converting Bluetooth or Barometer Data " + str(e))

            # get data from GPS
            # get data from Accelerometer

            lora_rcv = self.lora.receive()
            if lora_rcv:
                print('Received message from LoRa: ' + str(lora_rcv))
            utime.sleep(0.5)

