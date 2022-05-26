from files.modules.lora import LoRa
from files.modules.gsm import GSM
from files.utils.logger import Logger
import utime

class Base:
    def __init__(self):
        self.log = Logger()
        self.lora = LoRa(
            uart_num=1,
            tx_pin=4,
            rx_pin=5,
            m0=6,
            m1=7,
            log=self.log
        )
        self.gsm = GSM(
            tx_pin=16,
            rx_pin=17,
            power_pin=22,
            debug=True,
            carrier='timbrasil.br',
            carrier_usr='tim',
            carrier_pwd='tim',
            srv_endpoint='http://fall-guys-integration-workship.herokuapp.com',
            srv_user='x'
        )
        self.gsm.sleep()
        # self.gsm._disconnect_internet()

    def run(self):
        print("Waiting LoRa...")
        position = "stand"
        while True:
            rcv_msg = self.lora.receive()
            if rcv_msg and rcv_msg != "":
                print(rcv_msg)
                if "type" in rcv_msg.keys():
                    type = rcv_msg['type']
                    print(type)
                # if type == 'GPS':
                #     self.gsm.send_data(None, [rcv_msg['lat'], rcv_msg['lon']], None)
                # if type == 'ACC':
                #     self.gsm.send_data(rcv_msg['steps'], None, None)
                    if type == 'BAR':
                        if "fall" in rcv_msg.keys() and rcv_msg['fall'] and position != "fall":
                            print("send notification to server - Fall")
                            self.gsm.reboot()
                            self.gsm.send_sms("041992238508", "Fall")
                            self.gsm._connect_internet()
                            self.gsm.send_notification('fall')
                            self.gsm._disconnect_internet()
                            self.gsm.sleep()
                            position = "fall"
                        elif position == "fall":
                            self.gsm.reboot()
                            position = "stand"
                            print("send notification to server - Stand")
                            self.gsm._connect_internet()
                            self.gsm.send_notification('stand')
                            self.gsm._disconnect_internet()
                            self.gsm.sleep()

                    if type == 'BUT':
                        self.gsm.reboot()
                        print("send notification to server - Button")
                        self.gsm._connect_internet()
                        self.gsm.send_sms("041992238508", "Alert Button")
                        self.gsm.send_notification('panic')
                        self.gsm._disconnect_internet()
                        self.gsm.sleep()

            utime.sleep(0.02)
