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

        self.serialport = serial.Serial(port=port,
                                        baudrate=baud,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS,
                                        timeout=1)


    def __del__(self):
        """Destructor for the Serial transport, closing all resources."""
        try:
            self.serialport.close()
        except:
            pass


    def _to_byte_array(self, data):
        """Encodes an input string or list of values/characters into a flat
           byte array of bytes. This can be used to convert a Unicode string
           (using an ASCII only encoding) or list of characters and integers
           into a flat set of bytes for transmission.

           Args:
              data : input data to convert

           Returns:
              Flat byte array.
        """

        if isinstance(data, str):
            return bytearray(data.encode('ascii', 'ignore'))
        else:
            return bytearray([ord(d) if isinstance(d, str) else d for d in data])


    def read(self, length):
        """Reads a given number of bytes from the serial interface.

            Args:
                length : Number of bytes to read.

            Returns:
                Byte array of the received data.

            Raises:
                TimeoutError if the read operation timed out.
        """

        data = self.serialport.read(length)
        if len(data) != length:
            raise Transport.TimeoutError()

        self.LOG.debug('Receive %d bytes %s' % (len(data), [b for b in data]))

        return bytearray(data)


    def write(self, data):
        """Writes a given number of bytes to the serial interface.

            Args:
                data : Bytes to write.
        """

        self.LOG.debug('Send %d bytes: %s' % (len(data), [b for b in data]))

        self.serialport.write(self._to_byte_array(data))
