from files.modules.lora import LoRa
from files.utils.logger import Logger
import utime

class Base:
    def __init__(self):
        self.log = Logger()
        self.lora = LoRa(
            uart_num=0,
            tx_pin=0,
            rx_pin=1,
            log=self.log
        )

    def run(self):
        while True:
            rcv_msg = self.lora.receive()
            if rcv_msg:
                self.log.info('Received message from LoRa '+ str(rcv_msg))
                if 'F' in rcv_msg:
                    print('FALL DETECTED')
                    self.log.info('FALL DETECTED')
                elif 'B' in rcv_msg:
                    print('BUTTON PRESSED')
                    self.log.info('BUTTON PRESSED')
            utime.sleep(0.2)
