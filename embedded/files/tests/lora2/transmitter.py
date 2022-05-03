import utime
from machine import UART
from files.utils.blink_led import blink_led

# https://www.youtube.com/watch?v=BEAHCSFP2OQ
# https://www.micropeta.com/video24

def send(string):
    lora = UART(0, 9600)
    blink_led(0.2)
    bytes_sent = lora.write(string)
    print("Bytes sent:", bytes_sent)
    utime.sleep(1)

def receive():
    lora = UART(0, 9600)
    blink_led(0.2)
    dataRead = lora.readline()
    print(dataRead)
    utime.sleep(0.2)


if __name__ == "__main__":
    send("TESTE")
