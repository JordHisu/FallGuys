from files.utils.smbus import SMBus
from utime import ticks_ms

# ADXL345 constants
EARTH_GRAVITY_MS2 = 9.80665
SCALE_MULTIPLIER = 0.004

DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D

BW_RATE_1600HZ = 0x0F
BW_RATE_800HZ = 0x0E
BW_RATE_400HZ = 0x0D
BW_RATE_200HZ = 0x0C
BW_RATE_100HZ = 0x0B
BW_RATE_50HZ = 0x0A
BW_RATE_25HZ = 0x09
BW_RATE_125HZ = 0x08

RANGE_2G = 0x00
RANGE_4G = 0x01
RANGE_8G = 0x02
RANGE_16G = 0x03

MODE_STREAM = 0x40
MODE_FIFO = 0x80
MOD_TRIGGER = 0xC0

MEASURE = 0x08
AXES_DATA = 0x32
FIFO_MODE = 0x38


class Accelerometer:
    address = None
    nvalues = 20
    threshold = 4
    minacc = 1.5
    step_delay_ms = 1000

    def __init__(self, i2c, log, address=0x53, irq_callback=None, i2c_lock=None):
        self.i2c = i2c
        self.bus = SMBus(self.i2c, i2c_lock)

        self.log = log
        self.callback = irq_callback
        self.address = address

        self.setBandwidthRate(BW_RATE_25HZ)
        self.setRange(RANGE_2G)
        self.enableMeasurement()
        self.enableStreamMode()

        self.xvalues = []
        self.yvalues = []
        self.zvalues = []
        self.avalues = []
        self.intxvalues = 0
        self.intyvalues = 0
        self.intzvalues = 0
        self.intavalues = 0
        self.validationstep = 0

        self.last_step_time = ticks_ms()

    def enableStreamMode(self):
        self.bus.write_byte_data(self.address, FIFO_MODE, MODE_STREAM)

    def enableMeasurement(self):
        self.bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        self.bus.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = self.bus.read_byte_data(self.address, DATA_FORMAT)[0]

        value = value & 0x0F
        value |= range_flag
        value |= 0x08

        self.bus.write_byte_data(self.address, DATA_FORMAT, value)

    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce=False):
        bytes_ = self.bus.read_i2c_block_data(self.address, AXES_DATA, 6)
        if bytes_ is None:
            return

        x = bytes_[0] | (bytes_[1] << 8)
        if x & (1 << 16 - 1):
            x = x - (1 << 16)

        y = bytes_[2] | (bytes_[3] << 8)
        if y & (1 << 16 - 1):
            y = y - (1 << 16)

        z = bytes_[4] | (bytes_[5] << 8)
        if z & (1 << 16 - 1):
            z = z - (1 << 16)

        x = x * SCALE_MULTIPLIER
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if not gforce:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

    def stepIteration(self):
        axes = self.getAxes()
        if axes is None:
            return

        x = axes['x']
        y = axes['y']
        z = axes['z']

        if self.minacc > x > -self.minacc:
            x = 0
        if self.minacc > y > -self.minacc:
            y = 0
        if self.minacc > z > -self.minacc:
            z = 0

        self.xvalues.append(x)
        self.intxvalues += x
        self.yvalues.append(y)
        self.intyvalues += y
        self.zvalues.append(z)
        self.intzvalues += z

        count = len(self.xvalues)

        if count <= self.nvalues:
            return

        self.intxvalues -= self.xvalues.pop(0)
        self.intyvalues -= self.yvalues.pop(0)
        self.intzvalues -= self.zvalues.pop(0)
        
        gx = self.intxvalues / (count - 1)
        gy = self.intyvalues / (count - 1)
        gz = self.intzvalues / (count - 1)

        x -= gx
        y -= gy
        z -= gz

        a = x * (gy - gz) - y * (gx + gz) + z * (gx + gy)
        
        self.avalues.append(a)
        self.intavalues += a

        count = len(self.avalues)
        if count > self.nvalues:
            self.intavalues -= self.avalues.pop(0)
        
        if count <= 1:
            return

        a = self.intavalues / (count - 1)

        if self.last_step_time + self.step_delay_ms < ticks_ms() and abs(a) > self.threshold:
            self.last_step_time = ticks_ms()
            self.callback()

