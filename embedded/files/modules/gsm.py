from machine import UART, Pin
from utime import ticks_ms, sleep
import json
import re

NEW_LINE = "\r\n"
BAUDRATE = 115200


class GSM:
    def __init__(self, tx_pin=16, rx_pin=17, power_pin=22, debug=False, srv_endpoint='http://fall-guys-integration-workship.herokuapp.com', srv_user='c'):

        self.modem = UART(0, BAUDRATE, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.power = Pin(power_pin, Pin.OUT)
        self.debug = debug

        self.srv_endpoint = srv_endpoint
        self.srv_user = srv_user

        self.reboot()

    def exec(self, command, timeout_ms=1500, eol=NEW_LINE, ok_check=True):
        response = self.query(command, timeout_ms, eol)
        if ok_check:
            if "OK" not in response:
                raise Exception("Unknown response for '%s': %s" %
                                (command, response))
        return response

    def query(self, command, timeout_ms=1500, eol=NEW_LINE):
        if self.debug:
            print("[Debug GSM] AT Write - %s\n" % command)
        self.modem.write((command + eol).encode())
        sleep(0.01)
        response = self._read_buffer(timeout_ms)
        sleep(0.01)
        if self.debug:
            print("[Debug GSM] AT Read - %s\n" % response)
        return response

    def send_sms(self, number, message, timeout_ms=5000):
        if self.debug:
            print("[Debug GSM] - send_sms")
        response = self.query('AT+CMGS="%s"' % number, eol="\n")
        if ">" not in response:
            raise Exception("Unknown response: %s" % response)
        self.exec(message, timeout_ms, eol="\x1A")

    def reboot(self):
        self._power_cycle()
        self._configure_modem()
        self._ensure_connected_to_network()

    def _power_cycle(self):
        if self.debug:
            print("[Debug GSM] - _power_cycle")
        self.power.value(0)
        sleep(0.2)
        self.power.value(1)

    def sleep(self):
        self.power.value(0)

    def send_notification(self, not_type, disconnect=True):  # fall, stand, lying, panic
        if self.debug:
            print("[Debug GSM] - send_notification")
        url = f'{self.srv_endpoint}/sendnotif/{self.srv_user}'
        body = '{"type": "' + not_type + '"}'
        self.http_post(url, body)
        if disconnect:
            self._disconnect_internet()

    def get_configuration(self, disconnect=True):
        if self.debug:
            print("[Debug GSM] - get_configuration")
        url = f'{self.srv_endpoint}/getconfig/{self.srv_user}'
        res = self.http_get(url)
        search_res = re.search("{.*}", res)
        list_res = json.loads(search_res.group(0))
        config = {item[0]: item[1] for item in list_res["content"]}
        if disconnect:
            self._disconnect_internet()
        return config

    def get_info(self, disconnect=True):
        if self.debug:
            print("[Debug GSM] - get_info")
        url = f'{self.srv_endpoint}/info/{self.srv_user}'
        res = self.http_get(url)
        search_res = re.search("{.*}", res)
        list_res = json.loads(search_res.group(0))
        if disconnect:
            self._disconnect_internet()
        return list_res

    def send_data(self, steps, live_location, pressure, disconnect=True):
        if self.debug:
            print("[Debug GSM] - send_data")
        body_dict = {
            "steps": steps,
            "livelocation": live_location,
            "pressure": pressure
        }
        body = json.dumps(body_dict)
        url = f'{self.srv_endpoint}/senddata/{self.srv_user}'
        self.http_post(url, body)
        if disconnect:
            self._disconnect_internet()

    def http_get(self, url, timeout=10000, attempts=3):
        while attempts > 0:
            try:
                if self.debug:
                    print("[Debug GSM] - http_get")
                self._ensure_connected_to_internet()
                self.exec(f'AT+HTTPPARA="URL","{url}"')
                res = self.exec('AT+HTTPACTION=0', timeout_ms=timeout)
                if '200' not in res:
                    raise Exception(f"GSM - Unknown http get response code: {res}")
                result = self.exec('AT+HTTPREAD', timeout_ms=5000)
                return result
            except:
                attempts -= 1
                self.reboot()

    def http_post(self, url, body, timeout=10000, attempts=3):
         while attempts > 0:
            try:
                if self.debug:
                    print("[Debug GSM] - http_post")
                self._ensure_connected_to_internet()
                self.exec('AT+HTTPPARA="CONTENT",application/json')
                self.exec(f'AT+HTTPPARA="URL","{url}"')
                str_bytes = (body + "\n").encode()
                self.exec(f'AT+HTTPDATA={str(len(str_bytes))},10000', timeout_ms=3000, ok_check=False)
                self.modem.write(str_bytes)
                sleep(0.1)
                res = self.exec('AT+HTTPACTION=1', timeout_ms=timeout)
                if '200' not in res:
                    raise Exception(f"GSM - Unknown http post response code: {res}")
            except:
                attempts -= 1
                self.reboot()

    def _connect_internet(self, attempts=1000):
        if self.debug:
            print("[Debug GSM] - _connect_internet")
        while attempts > 0:
            try:
                self.exec('AT+SAPBR=1,1')
                self.exec('AT+SAPBR=2,1')  # Only to check current ip
                self.exec('AT+HTTPINIT')
                self.exec('AT+HTTPPARA="CID",1')
                sleep(1)
                return
            except:
                attempts -= 1
                sleep(3)
        raise Exception("GSM - Unable to connect to internet")

    def _disconnect_internet(self):
        if self.debug:
            print("[Debug GSM] - _disconnect_internet")
        try:
            self.exec('AT+HTTPTERM')
            self.exec('AT+SAPBR=0,1')
        except Exception as e:
            print('GSM - _disconnect_internet error -> ', str(e))

    def _configure_modem(self, attempts=1000):
        if self.debug:
            print("[Debug GSM] - _configure_modem")
        while attempts > 0:
            try:
                self.exec("AT")  # Check modem ready
                self.exec("ATE1")  # Enable command echo
                self.exec("AT+CMGF=1")  # Enable 'text' mode for SMS
                self.exec('AT+SAPBR=3,1,"Contype","GPRS"')  # Enable 'GPRS' mode for internet connection
                return
            except:
                attempts -= 1
                sleep(1)
        raise Exception("GSM - Unable to configure modem")

    def _ensure_connected_to_internet(self):
        if self.debug:
            print("[Debug GSM] - _ensure_connected_to_internet")
        try:
            res = self.exec('AT+SAPBR=2,1')
            search_res = re.search('\+SAPBR: (\d),(\d)', res)
            bearer_status = search_res.group(2)
            if bearer_status == '1':
                return
        except Exception as e:
            print(f'GSM - Failed to verify internet connection status: {e}')
        self._connect_internet()

    def _ensure_connected_to_network(self, attempts=1000):
        if self.debug:
            print("[Debug GSM] - _ensure_connected_to_network")
        while attempts > 0:
            try:
                network_response = self.query("AT+COPS?").split(NEW_LINE)[1]
                if "+COPS:" in network_response and "," in network_response:
                    return
            except:
                attempts -= 1
                sleep(1)
        raise Exception("Failed to connect")

    def _read_buffer(self, timeout_ms):
        if self.debug:
            print("[Debug GSM] - _read_buffer")
        buffer = bytes()
        now = ticks_ms()
        while (ticks_ms() - now) < timeout_ms and len(buffer) < 1025:
            if self.modem.any():
                buffer += self.modem.read(1)
        return buffer.decode()
