
from machine import Pin
from utime import sleep


def blink_led(time=1):
    led = Pin(25, Pin.OUT)
    led.on()
    sleep(time)
    led.off()
    sleep(time)


if __name__ == "__main__":
    blink_led()

