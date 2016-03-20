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

    def __init__(self, transport):
        """Instantiates a SAMBA instance with a given transport, ready for use.

           Args:
               transport : Transport connected to a SAM-BA device.
        """

        self.transport = transport

        self._execute(SAMBACommands.SET_NORMAL_MODE, read_length=2)


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


    def _execute(self, command, arguments=None, read_length=None):
        """Executes a low level SAM-BA command, sending the command and
           parameters to the device and reading back the response.

           Args:
               command     : `SAMBACommands` command to issue
               arguments   : List of one or two arguments to send with the
                             command, or `None` if no arguments should be sent.
               read_length : Number of response bytes that are expected.

           Returns:
               Read response from the device after the command was issued.
        """

        if arguments is None or len(arguments) is 0:
            arguments = ''
        elif len(arguments) is 1:
            arguments = self._to_32bit_hex(arguments[0]) + ','
        elif len(arguments) is 2:
            arguments = self._to_32bit_hex(arguments[0]) + ',' + self._to_32bit_hex(arguments[1])
        else:
            raise AssertionError("Invalid SAMBA command argument count: %d" % len(arguments))

        data = "%s%s#" % (command, arguments)

        self.transport.write(data)
        return self.transport.read(read_length)


    def run_from_address(self, address):
        """Starts execution in the attached device from the specified address.

           Args:
               address : Address in the attached device to run from
        """

        self._execute(SAMBACommands.GO, arguments=[address], read_length=0)


    def get_version(self):
        """Retrieves the SAM-BA version string from the attached device.

           Returns:
               Version string returned by the attached device.
        """

        return self._execute(SAMBACommands.GET_VERSION).strip()


    def write_word(self, address, word):
        """Writes a 32-bit word of data to the attached device.

           Args:
               address : Address to write the word at.
               word    : 32-bit word of data to write
        """

        self._execute(SAMBACommands.WRITE_WORD, arguments=[address, word], read_length=0)


    def read_word(self, address):
        """Reads a 32-bit word of data from the attached device.

           Args:
               address : Address to read the word from.

           Returns:
               Word of data read from the attached device.
        """

        word = self._execute(SAMBACommands.READ_WORD, arguments=[address], read_length=4)
        return struct.unpack("<I", word)[0]


    def write_half_word(self, address, half_word):
        """Writes a 16-bit half-word of data to the attached device.

           Args:
               address   : Address to write the half-word at.
               half_word : 16-bit half-word of data to write
        """
        self._execute(SAMBACommands.WRITE_HALF_WORD, arguments=[address, half_word], read_length=0)


    def read_half_word(self, address):
        """Reads a 16-bit half-word of data from the attached device.

           Args:
               address : Address to read the half-word from.

           Returns:
               Half-word of data read from the attached device.
        """

        half_word = self._execute(SAMBACommands.READ_HALF_WORD, arguments=[address], read_length=2)
        return struct.unpack("<H", half_word)[0]


    def write_byte(self, address, byte):
        """Writes an 8-bit byte of data to the attached device.

           Args:
               address : Address to write the byte at.
               byte    : Byte of data to write
        """

        self._execute(SAMBACommands.WRITE_BYTE, arguments=[address, byte], read_length=0)


    def read_byte(self, address):
        """Reads a byte of data from the attached device.

           Args:
               address : Address to read the byte from.

           Returns:
               Byte of data read from the attached device.
        """

        byte = self._execute(SAMBACommands.READ_BYTE, arguments=[address], read_length=1)
        return struct.unpack("<B", byte)[0]
