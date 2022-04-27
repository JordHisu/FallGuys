from files.utils.blink_led import blink_led
from _thread import start_new_thread
import utime


def print_loop(sleep_time=0.5):
    i = 0
    while True:
        print(f"Sleep time {sleep_time} - {i}")
        i += 1
        utime.sleep(sleep_time)


def led_blink_loop():
    while True:
        blink_led(0.7)


def run():
    start_new_thread(print_loop, ())
    led_blink_loop()

    # For semaphores, use lock = allocate_lock(), lock.acquire() and lock.release()
    # We can't use more than 2 threads because each one runs on its own core.


if __name__ == "__main__":
    run()
