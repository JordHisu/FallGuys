from machine import Pin, UART
import time, utime
from ubinascii import unhexlify


class GPS:
    def __init__(self, uart_num, tx_pin, rx_pin, enable_pin):
        self.enable = Pin(enable_pin, Pin.OUT)
        self.enable.value(1)
        
        self.uart = UART(uart_num, baudrate=9600, tx=Pin(tx_pin), rx=Pin(rx_pin))
        print("Trying to deactivate some GPS lines")
        self.uart.write(unhexlify("B56206040400FFFF02000E61"))                              # Cold start
        self.uart.write(unhexlify("2445494750512c5654472a32330d0ab56206010300f00500ff19"))  # GPVTG
        self.uart.write(unhexlify("2445494750512c4753562a32340d0ab56206010300f00300fd15"))  # GPGSV
        self.uart.write(unhexlify("2445494750512c524d432a33410d0ab56206010300f00400fe17"))  # GPRMC
        self.uart.write(unhexlify("2445494750512c4753412a33330d0ab56206010300f00200fc13"))  # GPGSA
        self.uart.write(unhexlify("2445494750512c474c4c2a32310d0ab56206010300f00100fb11"))  # GPGLL
        self.uart.write(unhexlify("B56206090D0000000000FFFF0000000000001731BF"))            # Save
        utime.sleep_ms(1000)
        print("Success... maybe")
        
        self.latitude = None
        self.longitude = None
        
    def convert_to_degree(self, raw_degrees):
        raw_as_float = float(raw_degrees)
        first_digits = int(raw_as_float/100) 
        next_two_digits = raw_as_float - float(first_digits*100)
        return float(first_digits + next_two_digits/60.0)
    
    def get_lat_lon(self):
        try:
            self._get_info_with_timeout(timeout_in_seconds=8)
        except Exception as e:
            print('Error getting GPS lat and lon ' + str(e))
        return self.latitude, self.longitude

    def _get_info_with_timeout(self, timeout_in_seconds):
        time_limit = time.time() + timeout_in_seconds
        while time.time() < time_limit:
            if self._read_uart():
                break
            utime.sleep_ms(500)

    def _read_uart(self):
        if not self.uart.any():
            return False

        text = self.uart.read().decode('utf-8')
        lines = text.split('\n')
        info = None
        for line in lines:
            if line.startswith('$GPGGA'):
                info = line.split(',')
                break
        else:
            return False

        lat = self.convert_to_degree(info[2])
        if info[3] == 'S':
            lat *= -1

        lon = self.convert_to_degree(info[4])
        if info[5] == 'W':
            lon *= -1

        self.latitude = self._format_coordinate(lat)
        self.longitude = self._format_coordinate(lon)
        return True

    def _format_coordinate(self, lat_or_lon):
        return '{0:.6f}'.format(lat_or_lon)

