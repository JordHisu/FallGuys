from files.modules.lora import LoRa
from files.modules.gsm import GSM
from files.utils.logger import Logger
import utime

class Base:
    def __init__(self):
        self.log = Logger()
        self.lora = LoRa(
            uart_num=0,
            tx_pin=0,
            rx_pin=1,
            m0=6,
            m1=7,
            log=self.log
        )
        # self.gsm = GSM(
        #     tx_pin=16,
        #     rx_pin=17,
        #     power_pin=22,
        #     debug=False,
        #     carrier='timbrasil.br',
        #     carrier_usr='tim',
        #     carrier_pwd='tim',
        #     srv_endpoint='http://fall-guys-integration-workship.herokuapp.com',
        #     srv_user='c'
        # )

    def run(self):
        while True:
            rcv_msg = self.lora.receive()
            if rcv_msg:
                print(rcv_msg)
                # type = rcv_msg['type']
                # if type == 'GPS':
                #     self.gsm.send_data(None, [rcv_msg['lat'], rcv_msg['lon']], None)
                # if type == 'ACC':
                #     self.gsm.send_data(rcv_msg['steps'], None, None)
                # if type == 'BAR':
                #     print(rcv_msg)
                #     # send A to server
                # if type == 'BUT':
                #     self.gsm.send_notification('panic')

            utime.sleep(0.4)
