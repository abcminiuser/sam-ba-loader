#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import abc


"""Base class for SAM-BA transports. Derived instances should override all methods."""
class Transport(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def read(self):
        pass


    @abc.abstractmethod
    def write(self, data):
        pass


"""Serial transport for SAM-BA devices using a COM port."""
class SerialTransport(Transport):
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
                break

        return bytes(line)


    def read(self, length=None):
        if length is None:
            data = self._readline()
        else:
            data = self.serialport.read(length)

        if self.log_to_console:
            print '< ' + data

        return data


    def write(self, data):
        if self.log_to_console:
            print '> ' + data

        self.serialport.write(data)
        self.serialport.write('\n')

