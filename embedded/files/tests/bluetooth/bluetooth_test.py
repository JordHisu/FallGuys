import uos
import machine
import utime
from files.tests.bluetooth import bluetooth_pair

print(uos.uname())
tx = machine.Pin(12)
rx = machine.Pin(13)
tx1 = machine.Pin(8)
rx1 = machine.Pin(9)

uart0 = machine.UART(0, baudrate=9600, tx=tx, rx=rx)  # at-command
uart1 = machine.UART(1, baudrate=9600, tx=tx1, rx=rx1)  # at-comand


def clartBuf(uart=uart0):
    print("Clear UART buffer " + str(uart))
    while uart.any():
        print(uart.read(1))

def test():
    # indicate program started visually
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(0)  # onboard LED OFF/ON for 0.5/1.0 sec
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(1.0)
    led_onboard.value(0)

    print(uart0)
    print(uart1)

    clartBuf()
    clartBuf(uart1)

    uart1.write("1234567890abcdefghijklmnopqrstuvwxyz\r\n")

    prvMills = utime.ticks_ms()
    bUart0 = b''
    bUart1 = b''
    while (utime.ticks_ms() - prvMills) < 3000:
        if uart0.any():
            b0 = uart0.read(1)
            bUart0 = bUart0 + b0
            print("UART(0): " + b0.decode('utf-8'))
            uart0.write(b0.upper().decode('utf-8'))
        if uart1.any():
            b1 = uart1.read(1)
            bUart1 = bUart1 + b1
            print("UART(1): " + b1.decode('utf-8'))

    print("UART0: ")
    print(bUart0)
    print("UART1: ")
    print(bUart1)

    print("===========")
    if bUart0 == bUart1.lower():
        print("MATCH")
    else:
        print("UN-MATCH!!!")
    print("===========")

    print("- Done -")



def run():
    bluetooth_pair.run()
    test()