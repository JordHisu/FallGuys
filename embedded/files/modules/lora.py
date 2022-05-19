import machine

class LoRa:
    def __init__(self, uart_num, tx_pin, rx_pin, log):
        tx = machine.Pin(tx_pin)
        rx = machine.Pin(rx_pin)
        self.uart = machine.UART(uart_num, baudrate=9600, tx=tx, rx=rx)

        self.log = log

        self.log.info("LoRa UART: " + str(self.uart))

    def send(self, msg):
        try:
            print("Sending: " + str(msg))
            self.log.info("Sending by LoRa: " + str(msg))
            self.uart.write(str(msg))
        except Exception as e:
            self.log.error("Exception sending to LoRa: " + str(e))

    def receive(self):
        try:
            read = self.uart.readline()
            if read:
                decided = read.decode('utf-8')
                self.log.info("Received form LoRa: " + decided)
                return decided
        except Exception as e:
            self.log.error("Exception receiving from LoRa: " + str(e))
        return None



