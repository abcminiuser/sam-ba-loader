#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import FlashController


class NVMCTRL(FlashController.FlashController):
    CMDA_OFFSET      = 0x0000
    PARAM_OFFSET     = 0x0008
    STATUS_OFFSET    = 0x0018
    INTFLAG_OFFSET   = 0x0014
    ADDRESS_OFFSET   = 0x001C

    INTFLAG_READY    = (1 << 0)
    INTFLAG_ERROR    = (1 << 1)

    CMDA_COMMANDS    = {
        "ER" : 0x02,
        "WP" : 0x04,
    }

    PAGES_PER_ROW    = 4


    def __init__(self, base_address):
        self.base_address = base_address


    def _get_nvm_params(self, samba):
        nvm_param = samba.read_word(self.base_address + self.PARAM_OFFSET)

        self.page_size = 8 << ((nvm_param >> 16) & 0x07)
        self.pages     = nvm_param & 0xFFFF


    def _wait_while_busy(self, samba):
        while not samba.read_half_word(self.base_address + self.INTFLAG_OFFSET) & self.INTFLAG_READY:
            pass


    def _command(self, samba, command):
        self._wait_while_busy(samba)

        reg  = (0xA5 << 8) | command
        samba.write_half_word(self.base_address + self.CMDA_OFFSET, reg)


    def erase_chip(self, samba):
        self._get_nvm_params(samba)

        for p in xrange(0, self.pages, self.PAGES_PER_ROW):
            samba.write_word(self.base_address + self.ADDRESS_OFFSET, p)
            self._command(samba, self.CMDA_COMMANDS['ER'])

        self._wait_while_busy(samba)
