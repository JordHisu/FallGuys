from files.modules.lora import LoRa
from files.modules.gsm import GSM
from files.modules.barometer import Barometer
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
            debug=False,
            srv_endpoint='http://fall-guys-integration-workship.herokuapp.com',
            srv_user='a'
        )
        self.barometer = Barometer(
            i2c_num=1,
            scl_pin=3,
            sda_pin=2,
            log=self.log,
            address=0x77
        )
        
        try:
            print('INIT - Get info (number)')
            result = self.gsm.get_info(disconnect=False)
            self.cel_number = result["number"]
        except:
            print('Error getting phone number')
            # self.cel_number = '045999710704'
            self.cel_number = '041991044054'
            
        try:    
            print('INIT - Sending stand notification')
            self.gsm.send_notification('stand', disconnect=False)
        except:
            print('Error sending "stand" notification')
            
        self.first_time = True
        self.offset = 0

    def run(self):
        print("Waiting LoRa...")
        position = "stand"

        previous_lora = utime.ticks_ms()
        previous_led = utime.ticks_ms()
        previous_bar = utime.ticks_ms()

        while True:
            if utime.ticks_ms() - previous_led > 500:
                toggle_led()
                previous_led = utime.ticks_ms()
            if utime.ticks_ms() - previous_lora > 400:
                try:
                    rcv_msgs = self.lora.receive()
                    if rcv_msgs and rcv_msgs != "":
                        for rcv_msg in rcv_msgs:
                                if rcv_msg == 'Anklet is running':
                                    print("Anklet is running")
                                    self.gsm.send_sms(self.cel_number, "Anklet connected")
                                    previous_lora = utime.ticks_ms()
                                    continue
                                if "type" in rcv_msg.keys():
                                    type = rcv_msg["type"]
                                    if type == 'GPS':
                                        if 'lat' not in rcv_msg.keys() or 'lon' not in rcv_msg.keys():
                                            previous_lora = utime.ticks_ms()
                                            continue
                                        lat = rcv_msg['lat'] 
                                        lon = rcv_msg['lon'] 
                                        if lat == None or lon == None:
                                            lat = -25.4398898
                                            lon = -49.2683882
                                        print("send notification to server - GPS")
                                        self.gsm.send_data(None, [lat, lon], None, disconnect=False)
                                    elif type == 'ACC':
                                        print("send notification to server - Accelerometer")
                                        self.gsm.send_data(rcv_msg['steps'], None, None, disconnect=False)
                                    elif type == 'BAR':
                                        necklace = rcv_msg["necklace"]
                                        anklet = rcv_msg["anklet"]
                                        if "fall" in rcv_msg.keys():
                                            if rcv_msg['fall']:
                                                base = self.barometer.getAltitude() - self.offset
                                                barometer_media = (necklace+anklet)/2
                                                if self.first_time:
                                                    self.offset =  base - barometer_media
                                                    self.first_time = False
                                                    print("Devices calibrated! Everything ready to go")
                                                    self.gsm.send_sms(self.cel_number, "Devices calibrated! Everything ready to go")
                                                    previous_lora = utime.ticks_ms()
                                                    continue
                                                if barometer_media - base > 0.4 and barometer_media - base < 1.0:
                                                    if position == "lying":
                                                        previous_lora = utime.ticks_ms()
                                                        continue
                                                    position = "lying"
                                                    print("send notification to server - Lying")
                                                    self.gsm.send_notification("lying", disconnect=False)
                                                    self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
                                                elif position != "fall":
                                                    print("send notification to server - Fall")
                                                    position = "fall"
                                                    self.gsm.send_sms(self.cel_number, "Fall detected!!")
                                                    self.gsm.send_notification('fall', disconnect=False)
                                                    self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
                                            elif position == "fall" or position == "lying":
                                                position = "stand"
                                                print("send notification to server - Stand")
                                                self.gsm.send_notification('stand', disconnect=False)
                                                self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
                                            if utime.ticks_ms() - previous_bar > 240000:
                                                self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
                                                previous_bar = utime.ticks_ms()
                                    elif type == 'BUT':
                                        print("send notification to server - Button")
                                        self.gsm.send_sms(self.cel_number, "Panic button pressed!!")
                                        self.gsm.send_notification('panic', disconnect=False)
                                    else:
                                        print('Invalid LoRa message type: ' + str(type))
                except Exception as e:
                    print("Exception on main loop: " + str(e))
                previous_lora = utime.ticks_ms()
