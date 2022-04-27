import utime
from machine import UART


def run():
    lora = UART(0, 9600)
    for i in range(3):
        bytes_sent = lora.write("TESTE")
        print("Bytes sent:", bytes_sent)
        utime.sleep(0.5)


if __name__ == "__main__":
    run()
