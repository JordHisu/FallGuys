from files.tests.lora2.transmitter import send as lora_send
from files.utils.blink_led import blink_led
from _thread import start_new_thread
from files.tests import threading
from files.tests.lora2.transmitter import receive


def run():
    while True:
        receive()


if __name__ == "__main__":
    run()
