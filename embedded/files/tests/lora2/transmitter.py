import utime
from machine import UART

# https://www.youtube.com/watch?v=BEAHCSFP2OQ
# https://www.micropeta.com/video24

def send(string):
    lora = UART(0, 9600)
    for i in range(10):
        bytes_sent = lora.write(string)
        print("Bytes sent:", bytes_sent)
        utime.sleep(0.5)


if __name__ == "__main__":
    send("TESTE")
