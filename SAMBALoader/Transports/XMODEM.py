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
import io

try:
    xrange
except NameError:
    # Remap xrange to range for Python 3
    xrange = range


class XMODEM(Transport.TransportBase):
    """XMODEM wrapper transport."""

    def __init__(self, transport):
        try:
            import xmodem
        except ImportError as e:
            self.LOG.fatal('Could not import xmodem library. Is it installed?')
            raise e

        self.transport = transport
        self.xmodem    = xmodem.XMODEM(self._read_byte, self._write_byte)


    def _read_byte(self, size, timeout=1):
        return self.transport.read(size)


    def _write_byte(self, byte, timeout=1):
        self.transport.write(byte)
        return 1


    def read(self, length):
        data = io.BytesIO()
        self.xmodem.recv(data)
        return [ord(b) if isinstance(b, str) else b for b in data.getvalue()]


    def write(self, data):
        self.xmodem.send(data)
