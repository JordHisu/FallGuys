from machine import Pin, UART
import time, utime


class GPS:
    def __init__(self, uart_num, tx_pin, rx_pin, enable_pin):
        self.enable = Pin(enable_pin, Pin.OUT)
        self.enable.value(1)
        
        self.uart = UART(uart_num, baudrate=9600, tx=Pin(tx_pin), rx=Pin(rx_pin))
        
        self.latitude = None
        self.longitude = None
        
    def convert_to_degree(self, raw_degrees):

        raw_as_float = float(raw_degrees)
        first_digits = int(raw_as_float/100) 
        next_two_digits = raw_as_float - float(first_digits*100) 
        
        converted = float(first_digits + next_two_digits/60.0)
        converted = '{0:.6f}'.format(converted) 
        return str(converted)
    
    def get_lat_lon(self):
        
        timeout = time.time() + 8 
        
        while True:
            self.uart.readline()
            buff = str(self.uart.readline())
            parts = buff.split(',')
        
            if (parts[0] == "b'$GPGGA" and len(parts) == 15):
                if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                    
                    self.latitude = self.convert_to_degree(parts[2])
                    if (parts[3] == 'S'):
                        self.latitude = -self.latitude
                    self.longitude = self.convert_to_degree(parts[4])
                    if (parts[5] == 'W'):
                        self.longitude = -self.longitude
                    break
                    
            if (time.time() > timeout):
                break
            utime.sleep_ms(500)
            
        return self.latitude, self.longitude