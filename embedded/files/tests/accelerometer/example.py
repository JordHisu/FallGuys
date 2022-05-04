from time import sleep
from files.tests.accelerometer.adxl345 import ADXL345
from machine import Pin, I2C


def accelerometer():
    adxl345 = ADXL345()
    while True:
        axes = adxl345.getAxes(True)
        print("ADXL345 on address :" + str(adxl345.address))

        print(f"   x = {axes['x']}fG")
        print(f"   y = {axes['y']}fG")
        print(f"   z = {axes['z']}fG")
        sleep(1)