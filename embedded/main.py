from files.tests.lora2.transmitter import send as lora_send
from files.utils.blink_led import blink_led
from _thread import start_new_thread
from files.tests import threading
from files.tests.lora.server import setup_receiver


def run():
    # start_new_thread(lora_send, ("TESTE", ))
    setup_receiver()
    while True:
        blink_led()


if __name__ == "__main__":
    run()
