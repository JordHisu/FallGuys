import uos
import machine
import utime

print(uos.uname())

tx = machine.Pin(12)
rx = machine.Pin(13)
tx1 = machine.Pin(8)
rx1 = machine.Pin(9)

uart0 = machine.UART(0, baudrate=9600, tx=tx, rx=rx)  # at-command
uart1 = machine.UART(1, baudrate=9600, tx=tx1, rx=rx1)  # at-comand


# 2 sec timeout is arbitrarily chosen
def sendCMD_waitResp(cmd, uart=uart1, timeout=50):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()

def send(msg, uart=uart1):
    print("Sending: " + msg)
    uart.write(msg)
    print()


def waitResp(uart=uart1, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms() - prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)

def run():
    # indicate program started visually
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(0)  # onboard LED OFF/ON for 0.5/1.0 sec
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(1.0)
    led_onboard.value(0)

    print(uart0)
    print(uart1)

    utime.sleep(2)

    print("- uart0 -")
    waitResp()
    sendCMD_waitResp("AT+RESET\r\n", uart0)  # Restore default setting
    sendCMD_waitResp("AT+PERM10110\r\n", uart0)  # Restore default setting
    sendCMD_waitResp("AT+PERM\r\n", uart0)  # Restore default setting

    sendCMD_waitResp("AT+ROLE\r\n", uart0)
    sendCMD_waitResp("AT+ROLE0\r\n", uart0) # Slave
    sendCMD_waitResp("AT+ROLE\r\n", uart0)

    sendCMD_waitResp("AT+NAME\r\n", uart0)
    sendCMD_waitResp("AT+NAMEJDY-18S\r\n", uart0)
    sendCMD_waitResp("AT+NAME\r\n", uart0)

    sendCMD_waitResp("AT+PIN\r\n", uart0)
    sendCMD_waitResp("AT+PIN000000\r\n", uart0)
    sendCMD_waitResp("AT+PIN\r\n", uart0)

    sendCMD_waitResp("AT+NAME\r\n", uart0)

    print("- uart1 -")
    waitResp(uart1)

    sendCMD_waitResp("AT+RESET\r\n", uart1)  # Restore default setting
    sendCMD_waitResp("AT+PERM10110\r\n", uart1)  # Restore default setting
    sendCMD_waitResp("AT+PERM\r\n", uart1)  # Restore default setting

    sendCMD_waitResp("AT+ROLE\r\n", uart1)
    sendCMD_waitResp("AT+ROLE1\r\n", uart1) # Master
    sendCMD_waitResp("AT+ROLE\r\n", uart1)

    sendCMD_waitResp("AT+NAME\r\n", uart1)
    sendCMD_waitResp("AT+NAMEJDY-18M\r\n", uart1)
    sendCMD_waitResp("AT+NAME\r\n", uart1)

    sendCMD_waitResp("AT+PIN\r\n", uart1)
    sendCMD_waitResp("AT+PIN000000\r\n", uart1)
    sendCMD_waitResp("AT+PIN\r\n", uart1)

    sendCMD_waitResp("AT+NAME\r\n", uart1)

    sendCMD_waitResp("AT+INQ\r\n", uart1, 2000)

    sendCMD_waitResp("AT+CONN3CA551936A40\r\n", uart1, 2000)


    print("Done")