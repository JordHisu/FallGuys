import machine
import json
import utime

class LoRa:
    def __init__(self, uart_num, tx_pin, rx_pin, m0, m1, log):
        tx = machine.Pin(tx_pin)
        rx = machine.Pin(rx_pin)

        self.m0 = machine.Pin(m0, machine.Pin.OUT)
        self.m1 = machine.Pin(m1, machine.Pin.OUT)

        self.m0.value(0)
        self.m1.value(0)

        self.uart = machine.UART(uart_num, baudrate=9600, tx=tx, rx=rx)

        self.log = log

        self.log.info("LoRa UART: " + str(self.uart))

        self.last_msg = ""


    def send(self, msg):
        try:
            print("Sending: " + str(msg))
            self.log.info("Sending by LoRa: " + str(msg))
            msg = msg
            str_send = json.dumps(msg) + "\n"
            self.uart.write(str(str_send))
            utime.sleep(0.02)
        except Exception as e:
            print("Exception sending to LoRa: " + str(e))
            self.log.error("Exception sending to LoRa: " + str(e))

    def receive(self):
        result = None
        try:
            read = self.uart.readline()
            if read:
                decoded = read.decode('utf-8')
                self.last_msg += decoded
                if '\n' not in self.last_msg :
                    return
                decoded_splited = self.last_msg.split("\n")
                self.last_msg = decoded_splited[-1]
                result = []
                for i in range(len(decoded_splited)-1):
                    self.log.info("Received form LoRa: " + decoded)
                    # print("Received form LoRa: " + str(decoded))
                    return_json = json.loads(decoded_splited[i])
                    result.append(return_json)
                return result
        except Exception as e:
            print("Exception receiving from LoRa: " + str(e))
            self.log.error("Exception receiving from LoRa: " + str(e))
        return result




