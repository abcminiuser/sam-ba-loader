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


    def read(self):
        data = self.serialport.readline()
        self.serialport.read(1)

        if self.log_to_console:
            print '< ' + data

        return data


    def write(self, data):
        if self.log_to_console:
            print '> ' + data

        self.serialport.write(data)
        self.serialport.write('\n')

