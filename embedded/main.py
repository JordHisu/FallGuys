from files.tests.lora2.transmitter import run as lora_transmit
from files.utils.blink_led import blink_led
from _thread import start_new_thread
import utime
from files.tests import threading


def run():
    threading.run()
    # start_new_thread(hey, ())
    # while True:
    #     blink_led()
    # start_new_thread(lora_transmit, ())
    # print("main.run() finished")


if __name__ == "__main__":
    run()
