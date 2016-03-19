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
    SET_NORMAL_MODE = 'N'
    GO              = 'G'
    GET_VERSION     = 'V'
    WRITE_WORD      = 'W'
    READ_WORD       = 'w'



class SAMBA(object):
    def __init__(self, transport):
        self.transport = transport

        self._execute(SAMBACommands.SET_NORMAL_MODE)


    def _to_32bit_hex(self, value):
        if not isinstance(value, str):
            value = "{0:0{1}x}".format(value, 8)

        return value


    def _execute(self, command, arguments=None, read_length=None):
        if arguments is None or len(arguments) is 0:
            arguments = ''
        elif len(arguments) is 1:
            arguments = self._to_32bit_hex(arguments[0]) + ','
        else:
            arguments = self._to_32bit_hex(arguments[1]) + ',' + self._to_32bit_hex(arguments[1])

        data = "%s%s#" % (command, arguments)

        self.transport.write(data)
        return self.transport.read(read_length)


    def run_from_address(self, address):
        self._execute(SAMBACommands.GO, [address])


    def get_version(self):
        return self._execute(SAMBACommands.GET_VERSION).strip()


    def write_word(self, address, word):
        word = struct.pack("<I", word)
        self._execute(SAMBACommands.WRITE_WORD, arguments=[address, word])


    def read_word(self, address):
        word = self._execute(SAMBACommands.READ_WORD, arguments=[address], read_length=4)
        return struct.unpack("<I", word)[0]
