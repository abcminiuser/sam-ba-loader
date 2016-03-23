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


class SerialTimeoutError(Exception):
    """Exception thrown when a read operation times out while waiting for more
       data.
    """
    pass


class Serial(Transport.TransportBase):
    """Serial transport for SAM-BA devices using a COM port."""

    def __init__(self, port, baud=115200, log_to_console=False):
        """Constructs a Serial transport.

           Args:
               port : Serial port to open (e.g. "COM1" or "/dev/ttyACM0").
               baud : Baud rate to use.
               log_to_console: If `True`, traffic will be logged to the console.
        """
        import serial

        self.serialport     = serial.Serial(port, baudrate=baud, timeout=1)
        self.log_to_console = log_to_console


    def __del__(self):
        """Destructor for the Serial transport, closing all resources."""
        self.serialport.close()


    def _readline(self):
        """Reads a line of text from the serial until the \n\r terminator.

           Returns:
               Line of serial data received, including terminator.

           Raises:
               SerialTimeoutError if the read operation timed out.
        """
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
        """Reads a given length of bytes from the serial interface.

            Args:
                length : Number of bytes to read.

            Returns:
                Byte array of the received data.

            Raises:
                SerialTimeoutError if the read operation timed out.
        """

        data = self.serialport.read(length)

        if len(data) != length:
            raise SerialTimeoutError()

        return bytes(data)


    def read(self, length=None):
        """Reads a given number of bytes from the serial interface.

            Args:
                length : Number of bytes to read. If `None`, a full line will be
                         read until a terminator is reached.

            Returns:
                Byte array of the received data.

            Raises:
                SerialTimeoutError if the read operation timed out.
        """

        if length is None:
            data = self._readline()
        else:
            data = self._read(length)

        if self.log_to_console:
            print '< ' + data

        return data


    def write(self, data):
        """Writes a given number of bytes to the serial interface.

            Args:
                data : Bytes to write.
        """

        if self.log_to_console:
            print '> ' + data

        self.serialport.write(data)
