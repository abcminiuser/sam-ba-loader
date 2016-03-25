#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

from . import Transport
import logging


class Serial(Transport.TransportBase):
    """Serial transport for SAM-BA devices using a COM port."""

    def __init__(self, port, baud=115200):
        """Constructs a Serial transport.

           Args:
               port : Serial port to open (e.g. "COM1" or "/dev/ttyACM0").
               baud : Baud rate to use.
               log_to_console: If `True`, traffic will be logged to the console.
        """

        try:
            import serial
        except ImportError as e:
            self.LOG.fatal('Could not import pyserial library. Is it installed?')
            raise e

        self.serialport = serial.Serial(port, baudrate=baud, timeout=1)


    def __del__(self):
        """Destructor for the Serial transport, closing all resources."""
        try:
            self.serialport.close()
        except:
            pass


    def read(self, length):
        """Reads a given number of bytes from the serial interface.

            Args:
                length : Number of bytes to read. If `None`, a full line will be
                         read until a terminator is reached.

            Returns:
                Byte array of the received data.

            Raises:
                SerialTimeoutError if the read operation timed out.
        """

        data = self.serialport.read(length)
        if len(data) != length:
            raise Transport.TimeoutError()

        self.LOG.debug('Receive %s' % [b for b in data])

        return bytes(data)


    def write(self, data):
        """Writes a given number of bytes to the serial interface.

            Args:
                data : Bytes to write.
        """

        self.LOG.debug('Send %s' % [b for b in data])

        self.serialport.write(data.encode('ascii', 'ignore'))
