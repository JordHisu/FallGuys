import time
from MS5611 import MS5611

## Basic Usage
sensor = MS5611(0)

## In a loop (10 times)
print()
while True:
    sum_temp = 0
    sum_press = 0
    times = 10
    for x in range(times):
        sensor.read()
        sum_temp += sensor.getTempC()
        sum_press += sensor.getPressureAdj()
        time.sleep(0.1)
    print("Values from sensor")
    print(str(sum_temp/times) + "C   " + str(sensor.convert2M(sum_press)/times) +  'm')

