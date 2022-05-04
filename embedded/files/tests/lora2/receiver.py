import utime
from machine import UART
from files.utils.blink_led import blink_led

def receive(lora):
    dataRead = lora.readline()
    if dataRead:
        print(dataRead.decode())
    utime.sleep(0.1)

if __name__ == "__main__":
    while True:
        receive()