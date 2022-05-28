
from machine import Pin
from utime import sleep


def blink_led(time=1):
    led = Pin(25, Pin.OUT)
    led.on()
    sleep(time)
    led.off()
    sleep(time)

def toggle_led():
    led = Pin(25, Pin.OUT)

    if bool(led.value()):
        led.off()
    else:
        led.on()


if __name__ == "__main__":
    blink_led()

