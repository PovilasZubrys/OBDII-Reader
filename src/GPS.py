import serial
import time

class Gps:

    def enable_serial():
        return serial.Serial('/dev/ttyS0', 115200, timeout=0)

    def enable_gps(serial):
        serial.write(b'AT+CGNSPWR=1\r\n')

    def get_gps_location(serial):
        serial.write(b'AT+CGNSINF\r\n')
        while True:
            response = serial.readline().decode('utf-8')

            if '+CGNSINF: 1,' in response:
                parts = response.split(',')

                return {'latitude': float(parts[3]), 'longitude': float(parts[4])}