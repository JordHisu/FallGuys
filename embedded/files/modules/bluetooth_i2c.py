import machine
import time


class Bluetooth:
    def __init__(self, i2c, log, address=0x50):
        self.i2c = i2c
        self.address = address
        self.log = log

        # mac = self.i2c.readfrom_mem(self.address, 0x11, 6)
        # time.sleep(0.05)
        # print('MODEL -> ' + str(mac))

    # def send(self, msg):
    #     print("Sending: " + str(msg))s
    #     self.i2c.writeto_mem(self.address, 0xF0, msg)  # Master

    def receive(self):
        rcv_length = self.i2c.readfrom_mem(self.address, 0xF1, 1)
        if rcv_length:
            rcv_length = int.from_bytes(rcv_length, 'big')
            if 0 < rcv_length < 255:
                rcv = self.i2c.readfrom_mem(self.address, 0xF2, rcv_length)
                if rcv:
                    return rcv.decode()
        return None


