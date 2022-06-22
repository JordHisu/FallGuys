class SMBus:
    def __init__(self, i2c, i2c_lock):
        self.i2c = i2c
        self.i2c_lock = i2c_lock

    def write_byte_data(self, address, memo_address, data):
        with self.i2c_lock:
            self.i2c.writeto_mem(address, memo_address, str(data))

    def read_byte_data(self, address, memo_address):
        with self.i2c_lock:
            return self.i2c.readfrom_mem(address, memo_address, 7)

    def read_i2c_block_data(self, address, memo_address, number_return):
        with self.i2c_lock:
            return self.i2c.readfrom_mem(address, memo_address, number_return)


