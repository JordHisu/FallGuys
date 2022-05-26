import machine
import utime

# Necklace (orange wire): 3CA551936A3B
# Anklet (white wire): 3CA551936A40

class Bluetooth:
    def __init__(self, name, uart_num, tx_pin, rx_pin, is_slave, log, device_to_connect="3CA551936A40"):
        tx = machine.Pin(tx_pin)
        rx = machine.Pin(rx_pin)
        self.uart = machine.UART(uart_num, baudrate=9600, tx=tx, rx=rx)

        self.log = log

        self.log.info("Bluetooth UART: " + str(self.uart))

        print("- uart -")
        self.waitResp()
        self.sendCMD_waitResp("AT+RESET\r\n")  # Restore default setting
        self.sendCMD_waitResp("AT+PERM10110\r\n")  # Restore default setting
        self.sendCMD_waitResp("AT+PERM\r\n")  # Restore default setting

        self.sendCMD_waitResp("AT+ROLE\r\n")
        if is_slave:
            self.sendCMD_waitResp("AT+ROLE0\r\n")  # Slave
        else:
            self.sendCMD_waitResp("AT+ROLE1\r\n")  # Master
        self.sendCMD_waitResp("AT+ROLE\r\n")

        self.sendCMD_waitResp("AT+NAME\r\n")
        self.sendCMD_waitResp("AT+NAME" + name + "\r\n")
        self.sendCMD_waitResp("AT+NAME\r\n")

        self.sendCMD_waitResp("AT+PIN\r\n")
        self.sendCMD_waitResp("AT+PIN000000\r\n")
        self.sendCMD_waitResp("AT+PIN\r\n")

        self.sendCMD_waitResp("AT+NAME\r\n")
        self.sendCMD_waitResp("AT+LADDR\r\n")

        if not is_slave:
            while True:
                self.sendCMD_waitResp("AT+INQ\r\n", 2000)
                response = self.sendCMD_waitResp("AT+CONN"+ device_to_connect + "\r\n", 2000)
                if response:
                    print('Bluetooth response: ' + str(response))
                    try:
                        if "CONNECTED" in response[:16].decode("utf-8"):
                            self.log.info('Connected via Bluetooth!')
                            break
                    except Exception as e:
                        self.log.error('Error trying to connect via Bluetooth ' + str(e))
                print("Not connected yet")

    def sendCMD_waitResp(self, cmd, timeout=50):
        print("CMD: " + cmd)
        self.uart.write(cmd)
        return self.waitResp(timeout)

    def waitResp(self, timeout=2000):
        prvMills = utime.ticks_ms()
        resp = b""
        while (utime.ticks_ms() - prvMills) < timeout:
            if self.uart.any():
                resp = b"".join([resp, self.uart.read(1)])
        print(resp)
        return resp

    def send(self, msg):
        print("Sending: " + str(msg))
        self.log.info("Sending by Bluetooth: " + str(msg))
        self.uart.write(str(msg + "\n"))
        print()

    def receive(self, timeout=500):
        prvMills = utime.ticks_ms()
        bUart = ""
        try:
            while (utime.ticks_ms() - prvMills) < timeout:
                if self.uart.any():
                    b0 = self.uart.read(1)
                    bUart = bUart + b0.decode('utf-8')
                    self.uart.write(b0.upper().decode('utf-8'))
            return bUart
        except Exception as e:
            self.log.error("Exception receiving from bluetooth: " + str(e))
        return None