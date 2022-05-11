
from machine import Pin, UART
from utime import sleep
import utime


def run():
    tx = Pin(12)
    rx = Pin(13)
    uart = UART(0, 9600, tx=tx, rx=rx)

    while True:
        if uart.any():
            sleep(0.5)
            command = clean_message(uart.readline().decode())
            print("RECEIVED:", command)
            if command:
                send("RECIVED: " + command, uart)
            if command == 'shutdown':
                break
    print("Shutting down")


def clean_message(message):
    valid_letter_list = [letter for letter in message if letter not in ('\t', '\n', '\r', '\v', '\f')]
    return "".join(valid_letter_list)

def send(cmd, uart):
    print("CMD: " + cmd)
    uart.write(cmd)
    print()


if __name__ == "__main__":
    run()
