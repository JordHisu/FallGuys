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
            debug=True,
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
        self.position = "stand"

        self.previous_lora = utime.ticks_ms()
        self.previous_led = utime.ticks_ms()
        self.previous_bar = utime.ticks_ms()

        while True:
            try:
                self.loop()
            except Exception as e:
                print('Error: ', str(e))
    
    def loop(self):
        self.toggle_led()
        self.receive_lora()

    def toggle_led(self):
        if not utime.ticks_ms() - self.previous_led > 500:
            return None
        toggle_led()
        self.previous_led = utime.ticks_ms()
    
    def receive_lora(self):
        if not utime.ticks_ms() - self.previous_lora > 400:
            return None

        rcv_msgs = self.lora.receive()
        if not rcv_msgs or rcv_msgs == "":
            self.previous_lora = utime.ticks_ms()
            return None

        for rcv_msg in rcv_msgs:
            if rcv_msg == 'Anklet is running':
                print("Anklet is running")
                self.gsm.send_sms(self.cel_number, "Anklet connected")
                self.previous_lora = utime.ticks_ms()
                continue
            if "type" in rcv_msg.keys():
                type = rcv_msg["type"]
                if type == 'GPS':
                    self.handle_gps(rcv_msg)
                    continue
                if type == 'ACC':
                    self.handle_accelerometer(rcv_msg)
                    continue
                if type == 'BAR':
                    self.handle_barometer(rcv_msg)
                    continue
                if type == 'BUT':
                    self.handle_button(rcv_msg)
                    continue

                print('Invalid LoRa message type: ' + str(type))

        print("Waiting LoRa...")
        self.previous_lora = utime.ticks_ms()

    def handle_gps(self, rcv_msg):
        print("GPS")
        if 'lat' not in rcv_msg.keys() or 'lon' not in rcv_msg.keys():
            return None
        lat = rcv_msg['lat'] 
        lon = rcv_msg['lon'] 
        if lat == None or lon == None:
            lat = -25.4398898
            lon = -49.2683882
        print("send notification to server - GPS")
        print("lat: ", lat, " lon:", lon)
        self.gsm.send_data(None, [lat, lon], None, disconnect=False)

    def handle_barometer(self, rcv_msg):
        necklace = rcv_msg["necklace"]
        anklet = rcv_msg["anklet"]
        if "fall" not in rcv_msg.keys():
            return None
        if rcv_msg['fall'] is True:
            base = self.barometer.getAltitude() - self.offset
            barometer_media = (necklace+anklet)/2
            if self.first_time:
                self.offset =  base - barometer_media
                self.first_time = False
                print("Devices calibrated! Everything ready to go")
                self.gsm.send_sms(self.cel_number, "Devices calibrated! Everything ready to go")
                return None
            if barometer_media - base > 0.4 and barometer_media - base < 1.0:
                if self.position == "lying":
                    return None
                self.position = "lying"
                print("send notification to server - Lying")
                self.gsm.send_notification("lying", disconnect=False)
                self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
                return None
            if self.position != "fall":
                print("send notification to server - Fall")
                self.position = "fall"
                self.gsm.send_sms(self.cel_number, "Fall detected!!")
                self.gsm.send_notification('fall', disconnect=False)
                self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
        if rcv_msg['fall'] is False and (self.position == "fall" or self.position == "lying"):
            self.position = "stand"
            print("send notification to server - Stand")
            self.gsm.send_notification('stand', disconnect=False)
            self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
            return None
        if utime.ticks_ms() - self.previous_bar > 240000:
            self.gsm.send_data(None, None, [anklet, base, necklace], disconnect=False)
            self.previous_bar = utime.ticks_ms()

    def handle_accelerometer(self, rcv_msg):
        print("send notification to server - Accelerometer")
        self.gsm.send_data(rcv_msg['steps'], None, None, disconnect=False)

    def handle_button(self, rcv_msg):
        print("send notification to server - Button")
        self.gsm.send_sms(self.cel_number, "Panic button pressed!!")
        self.gsm.send_notification('panic', disconnect=False)
