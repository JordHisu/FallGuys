import time
import math
import machine


class Barometer:
    def __init__(self, i2c_num, scl_pin, sda_pin, log, address=0x77, elevation=0):
        i2c = machine.I2C(i2c_num,
                          scl=machine.Pin(scl_pin),
                          sda=machine.Pin(sda_pin),
                          freq=400000)
        self.i2c = i2c
        self.elevation = elevation
        self.address = address
        self.log = log

    def setElevation(self, elevation):
        self.elevation = elevation

    def setElevationFt(self, elevation):
        self.elevation = elevation / 3.2808

    def setI2c(self, i2c):
        self.i2c = i2c

    def read(self):
        ## Get raw pressure
        self.i2c.writeto_mem(self.address, 0x48, "1")
        time.sleep(0.05)
        D1 = self.i2c.readfrom_mem(self.address, 0x00, 4)
        D1 = D1[0] * 65536 + D1[1] * 256.0 + D1[2]

        ## Get raw temperature
        self.i2c.writeto_mem(self.address, 0x58, "1")
        time.sleep(0.05)
        D2 = self.i2c.readfrom_mem(self.address, 0x00, 4)
        D2 = D2[0] * 65536 + D2[1] * 256.0 + D2[2]
        time.sleep(0.05)

        ## Read Constants from Sensor
        if hasattr(self, 'C1'):
            C1 = self.C1
        else:
            C1 = self.i2c.readfrom_mem(self.address, 0xA2, 4)  # Pressure Sensitivity
            C1 = C1[0] * 256.0 + C1[1]
            self.C1 = C1
            time.sleep(0.05)

        if hasattr(self, 'C2'):
            C2 = self.C2
        else:
            C2 = self.i2c.readfrom_mem(self.address, 0xA4, 4)  # Pressure Offset
            C2 = C2[0] * 256.0 + C2[1]
            self.C2 = C2
            time.sleep(0.05)

        if hasattr(self, 'C3'):
            C3 = self.C3
        else:
            C3 = self.i2c.readfrom_mem(self.address, 0xA6, 4)  # Temperature coefficient of pressure sensitivity
            C3 = C3[0] * 256.0 + C3[1]
            self.C3 = C3
            time.sleep(0.05)

        if hasattr(self, 'C4'):
            C4 = self.C4
        else:
            C4 = self.i2c.readfrom_mem(self.address, 0xA8, 4)  # Temperature coefficient of pressure offset
            C4 = C4[0] * 256.0 + C4[1]
            self.C4 = C4
            time.sleep(0.05)

        if hasattr(self, 'C5'):
            C5 = self.C5
        else:
            C5 = self.i2c.readfrom_mem(self.address, 0xAA, 4)  # Reference temperature
            C5 = C5[0] * 256.0 + C5[1]
            self.C5 = C5
            time.sleep(0.05)

        if hasattr(self, 'C6'):
            C6 = self.C6
        else:
            C6 = self.i2c.readfrom_mem(self.address, 0xAC, 4)  # Temperature coefficient of the temperature
            C6 = C6[0] * 256.0 + C6[1]
            self.C6 = C6
            time.sleep(0.05)

        ## These are the calculations provided in the datasheet for the sensor.
        dT = D2 - C5 * 2 ** 8
        TEMP = 2000 + dT * C6 / 2 ** 23

        ## Set Values to class to be used elsewhere
        self.tempC = TEMP / 100.0
        self.tempK = TEMP / 100.0 + 273.15

        ## These calculations are all used to produce the final pressure value
        OFF = C2 * 2 ** 16 + (C4 * dT) / 2 ** 7
        SENS = C1 * 2 ** 15 + (C3 * dT) / 2 ** 8
        P = (D1 * SENS / 2 ** 21 - OFF) / 2 ** 15
        self.pressure = P / 100.0

        ## Calculate an offset for the pressure.  This is required so that the readings are correct.
        ##   Equation can be found here: http://en.wikipedia.org/wiki/Barometric_formula
        altOffset = math.exp((-9.80665 * 0.0289644 * self.elevation) / (8.31432 * self.tempK))
        self.pressureAdj = (P / altOffset) / 100.0

    def getTempC(self):
        return self.tempC

    def getPressure(self):
        return self.pressure

    def getPressureAdj(self):
        return self.pressureAdj

    def printResults(self):
        print("Temperature:" + str(round(self.tempC, 2)) + "C")

        print("Pressure Absolute:" + str(round(self.pressure, 2)) + "hPa")
        print("         Adjusted:" + str(round(self.pressureAdj, 2)) + "hPa")
        print("         Adjusted:" + str(round(self.convert2In(self.pressureAdj), 2)) + "in")

    def convert2In(self, pressure):
        return pressure * 0.0295301

    def convert2M(self, pressure):
        return pressure * 0.0295301 * 254

    def getBarometerData(self):
        sum_temp = 0
        sum_press = 0
        times = 10
        for x in range(times):
            self.read()
            sum_temp += self.getTempC()
            sum_press += self.getPressureAdj()
            time.sleep(0.02)
        # print("Values from sensor")
        values_barometer = str(sum_temp / times) + "C   " + str(self.convert2M(sum_press) / times) + 'm'
        # print(values_barometer)
        self.log.info("Values from Barometer: " + values_barometer)
        return self.convert2M(sum_press) / times

