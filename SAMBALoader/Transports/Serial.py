#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import Transport


"""Exception thrown when the serial transport times out while waiting for more data."""
class SerialTimeoutError(Exception):
    pass


"""Serial transport for SAM-BA devices using a COM port."""
class Serial(Transport.Transport):
    def __init__(self, port, baud=115200, log_to_console=False):
        import serial

        self.serialport     = serial.Serial(port, baudrate=baud, timeout=1)
        self.log_to_console = log_to_console


    def __del__(self):
        self.serialport.close()


    def _readline(self):
        eol    = b'\n\r'
        leneol = len(eol)
        line   = bytearray()

        while True:
            c = self.serialport.read(1)

            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                raise SerialTimeoutError()

        return bytes(line)


    def _read(self, length):
        data = self.serialport.read(length)

        if len(data) != length:
            raise SerialTimeoutError()

        return bytes(data)


    def read(self, length=None):
        if length is None:
            data = self._readline()
        else:
            data = self._read(length)

        if self.log_to_console:
            print '< ' + data

        return data


    def write(self, data):
        if self.log_to_console:
            print '> ' + data

        self.serialport.write(data)
        self.serialport.write('\n')
