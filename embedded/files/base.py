from files.modules.lora import LoRa
from files.modules.gsm import GSM
from files.utils.logger import Logger
from files.utils.blink_led import toggle_led
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
            srv_endpoint='http://fall-guys-integration-workship.herokuapp.com',
            srv_user='a'
        )
        
        try:
            result = self.gsm.get_info()
            self.cel_number = result["number"]
        except:
            self.cel_number = '045999710704'
            
        try:    
            self.gsm.send_notification('stand')
        except:
            print('Error sending "stand" notification')

    def run(self):
        print("Waiting LoRa...")
        position = "stand"

        previous_lora = utime.ticks_ms()
        previous_led = utime.ticks_ms()

        while True:
            if utime.ticks_ms() - previous_led > 400:
                toggle_led()
                previous_led = utime.ticks_ms()
            if utime.ticks_ms() - previous_lora > 200:
                rcv_msgs = self.lora.receive()
                if rcv_msgs and rcv_msgs != "":
                    for rcv_msg in rcv_msgs:
                        print(rcv_msg)
                        try:
                            if "type" in rcv_msg.keys():
                                type = rcv_msg["type"]
                            # if type == 'GPS':
                            #     self.gsm.send_data(None, [rcv_msg['lat'], rcv_msg['lon']], None)
                            # if type == 'ACC':
                            #     self.gsm.send_data(rcv_msg['steps'], None, None)
                                if type == 'BAR':
                                    necklace = rcv_msg["necklace"]
                                    anklet = rcv_msg["anklet"]
                                    # verify barometer
                                    print(necklace, anklet)
                                    if "fall" in rcv_msg.keys():
                                        if rcv_msg['fall'] and position != "fall":
                                            print("send notification to server - Fall")
                                            self.gsm.send_sms(self.cel_number, "Fall")
                                            # self.gsm.send_sms("041992238508", "Fall")
                                            self.gsm.send_notification('fall')
                                            position = "fall"
                                        elif not rcv_msg['fall'] and position == "fall":
                                            position = "stand"
                                            print("send notification to server - Stand")
                                            self.gsm.send_notification('stand')

                                if type == 'BUT':
                                    print("send notification to server - Button")
                                    self.gsm.send_sms(self.cel_number, "Alert Button")
                                    self.gsm.send_notification('panic')
                        except:
                            print("Except")
                previous_lora = utime.ticks_ms()
