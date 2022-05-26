import machine
import json
import utime

class LoRa:
    def __init__(self, uart_num, tx_pin, rx_pin, m0, m1, log):
        tx = machine.Pin(tx_pin)
        rx = machine.Pin(rx_pin)
        self.uart = machine.UART(uart_num, baudrate=9600, tx=tx, rx=rx)

        self.m0 = machine.Pin(m0, machine.Pin.OUT)
        self.m1 = machine.Pin(m1, machine.Pin.OUT)

        self.m0.value(0)
        self.m1.value(0)

        self.log = log

        self.log.info("LoRa UART: " + str(self.uart))

    def send(self, msg):
        try:
            print("Sending: " + str(msg))
            self.log.info("Sending by LoRa: " + str(msg))
            str_send = json.dumps(msg) + "\n"
            self.uart.write(str(str_send))
            utime.sleep(0.05)
        except Exception as e:
            self.log.error("Exception sending to LoRa: " + str(e))

    def receive(self):
        try:
            read = self.uart.readline()
            if read:
                decoded = read.decode('utf-8')
                self.log.info("Received form LoRa: " + decoded)
                print("Received form LoRa: " + str(decoded))
                utime.sleep(0.05)
                return json.loads(decoded)
        except Exception as e:
            self.log.error("Exception receiving from LoRa: " + str(e))
        return None



