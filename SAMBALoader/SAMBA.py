#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import struct
import logging


class SAMBACommands:
    """Core SAM-BA bootloader commands."""

    SET_NORMAL_MODE = 'N'
    GO              = 'G'
    GET_VERSION     = 'V'
    WRITE_WORD      = 'W'
    READ_WORD       = 'w'
    WRITE_HALF_WORD = 'H'
    READ_HALF_WORD  = 'h'
    WRITE_BYTE      = 'O'
    READ_BYTE       = 'o'



class SAMBA(object):
    """Main SAM-BA instance, used to issue commands to an attached device over
       an established transport, and receive responses.
    """

    LOG = logging.getLogger(__name__)


    def __init__(self, transport):
        """Instantiates a SAMBA instance with a given transport, ready for use.

           Args:
               transport : Transport connected to a SAM-BA device.
        """

        self.transport = transport

        self.LOG.debug('Set normal mode');
        self.transport.write(self._serialize_command(SAMBACommands.SET_NORMAL_MODE, arguments=[]))
        self.transport.read(2)


    def _to_32bit_hex(self, value):
        """Internal helper function to convert a 32-bit value into a hex string,
           if it is not already in a string representation.

           Args:
               value : A value to convert.

           Returns:
               Hex encoded string of the input value.
        """

        if isinstance(value, str):
            return value
        else:
            return "%08x" % value


    def _serialize_command(self, command, arguments=None):
        """Executes a low level SAM-BA command, sending the command and
           parameters to the device and reading back the response.

           Args:
               command     : `SAMBACommands` command to issue
               arguments   : List of one or two arguments to send with the
                             command, or `None` if no arguments should be sent.

           Returns:
               Serialized SAMBA command with the embedded arguments (if any).
        """

        if arguments is None or len(arguments) is 0:
            arguments = ''
        elif len(arguments) is 1:
            arguments = self._to_32bit_hex(arguments[0]) + ','
        elif len(arguments) is 2:
            arguments = self._to_32bit_hex(arguments[0]) + ',' + self._to_32bit_hex(arguments[1])
        else:
            raise AssertionError('Invalid SAMBA command argument count: %d' % len(arguments))

        return '%s%s#' % (command, arguments)


    def run_from_address(self, address):
        """Starts execution in the attached device from the specified address.

           Args:
               address : Address in the attached device to run from
        """

        self.LOG.debug('Run @ 0x%08x' % address)
        self.transport.write(self._serialize_command(SAMBACommands.GO, arguments=[address]))


    def get_version(self):
        """Retrieves the SAM-BA version string from the attached device.

           Returns:
               Version string returned by the attached device.
        """

        self.transport.write(self._serialize_command(SAMBACommands.GET_VERSION, arguments=[]))

        version = bytearray()
        while True:
            version += self.transport.read(1)
            if b'\n\r' in version:
                break
        version = version.decode('ascii').strip()

        self.LOG.debug('Read Version = %s' % version)
        return version


    def write_word(self, address, word):
        """Writes a 32-bit word of data to the attached device.

           Args:
               address : Address to write the word at.
               word    : 32-bit word of data to write
        """

        self.transport.write(self._serialize_command(SAMBACommands.WRITE_WORD, arguments=[address, word]))
        self.LOG.debug('Write Word @ 0x%08x = 0x%08x' % (address, word))


    def read_word(self, address):
        """Reads a 32-bit word of data from the attached device.

           Args:
               address : Address to read the word from.

           Returns:
               Word of data read from the attached device.
        """

        self.transport.write(self._serialize_command(SAMBACommands.READ_WORD, arguments=[address]))
        word = struct.unpack("<I", self.transport.read(4))[0]

        self.LOG.debug('Read Word @ 0x%08x = 0x%08x' % (address, word))
        return word


    def write_half_word(self, address, half_word):
        """Writes a 16-bit half-word of data to the attached device.

           Args:
               address   : Address to write the half-word at.
               half_word : 16-bit half-word of data to write
        """

        self.transport.write(self._serialize_command(SAMBACommands.WRITE_HALF_WORD, arguments=[address, half_word]))
        self.LOG.debug('Write Half Word @ 0x%08x = 0x%04x' % (address, half_word))


    def read_half_word(self, address):
        """Reads a 16-bit half-word of data from the attached device.

           Args:
               address : Address to read the half-word from.

           Returns:
               Half-word of data read from the attached device.
        """

        self.transport.write(self._serialize_command(SAMBACommands.READ_HALF_WORD, arguments=[address]))
        half_word = struct.unpack("<H", self.transport.read(2))[0]

        self.LOG.debug('Read Half Word @ 0x%08x = 0x%04x' % (address, half_word))
        return half_word


    def write_byte(self, address, byte):
        """Writes an 8-bit byte of data to the attached device.

           Args:
               address : Address to write the byte at.
               byte    : Byte of data to write
        """

        self.transport.write(self._serialize_command(SAMBACommands.WRITE_BYTE, arguments=[address, byte]))
        self.LOG.debug('Write Byte @ 0x%08x = 0x%02x' % (address, byte))


    def read_byte(self, address):
        """Reads a byte of data from the attached device.

           Args:
               address : Address to read the byte from.

           Returns:
               Byte of data read from the attached device.
        """

        self.transport.write(self._serialize_command(SAMBACommands.READ_BYTE, arguments=[address]))
        byte = struct.unpack("<B", self.transport.read(1))[0]

        self.LOG.debug('Read Byte @ 0x%08x = 0x%02x' % (address, byte))
        return byte
