from files.tests.lora2.transmitter import send as lora_send
from files.utils.blink_led import blink_led
from _thread import start_new_thread
from files.tests import threading
from files.tests.lora2.transmitter import receive
from files.tests.accelerometer.example import accelerometer


def run():
    while True:
        accelerometer()


if __name__ == "__main__":
    run()
