from files.utils.smbus import SMBus


class Bluetooth:
    def __init__(self, i2c, i2c_lock, log, address=0x50):
        self.i2c = i2c
        self.address = address
        self.log = log
        self.smbus = SMBus(self.i2c, i2c_lock)

    def receive(self):
        rcv_length = self.smbus.read_i2c_block_data(self.address, 0xF1, 1)
        if not rcv_length:
            return None

        rcv_length = int.from_bytes(rcv_length, 'big')
        if not(0 < rcv_length < 255):
            return None

        rcv = self.smbus.read_i2c_block_data(self.address, 0xF2, rcv_length)
        if not rcv:
            return None

        return rcv.decode()


