#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

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


    def _execute(self, command, arguments=None):
        if not arguments is None:
            arguments = ','.join(self._to_32bit_hex(a) for a in arguments)
        else:
            arguments = ''

        data = "%s%s#" % (command, arguments)

        self.transport.write(data)
        return self.transport.read()


    def run_from_address(self, address):
        self._execute(SAMBACommands.GO, [address])


    def get_version(self):
        return self._execute(SAMBACommands.GET_VERSION).strip()


    def write_word(self, address, value):
        self._execute(SAMBACommands.WRITE_WORD, [address, value])


    def read_word(self, address):
        return self._execute(SAMBACommands.READ_WORD, [address, value])
