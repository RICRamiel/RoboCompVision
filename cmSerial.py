import serial
import time

class cmSerial:
    def __init__(self, path, baud_rate, ser_timeout=0.1, ser_w_timeout=0.1):
        self.ser = serial.Serial(path, baud_rate, timeout=ser_timeout, write_timeout=ser_w_timeout)

    def send_data(self, data):
        high_byte = 0
        low_byte = 0
        TxD_packet = bytearray(6)
        TxD_packet[0] = 0xff
        TxD_packet[1] = 0x55
        TxD_packet[2] = low_byte
        TxD_packet[3] = ~low_byte & 0xff
        TxD_packet[4] = high_byte
        TxD_packet[5] = ~high_byte & 0xff
        low_byte = data & 0xff
        TxD_packet[2] = low_byte & 0xff
        high_byte = (data >> 8) & 0xff
        TxD_packet[4] = high_byte & 0xff
        TxD_packet[5] = ~high_byte & 0xff
        if self.ser.write(TxD_packet) != 6:
            assert "FCK U", 'Can\'t send!'
        time.sleep(0.100)