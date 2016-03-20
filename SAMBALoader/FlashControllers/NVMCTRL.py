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
        "ER"  : 0x02,
        "WP"  : 0x04,
        "PBC" : 0x44
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


    def _clear_page_buffer(self, samba):
        self._wait_while_busy(samba)

        self._command(samba, self.CMDA_COMMANDS['PBC'])
        self._wait_while_busy(samba)


    def _command(self, samba, command):
        self._wait_while_busy(samba)

        reg  = (0xA5 << 8) | command
        samba.write_half_word(self.base_address + self.CMDA_OFFSET, reg)


    def erase_flash(self, samba, start_address=None, end_address=None):
        self._get_nvm_params(samba)

        if start_address is None:
            start_address = 0

        if end_address is None:
            end_address = self.pages * self.page_size

        start_address -= start_address % (self.PAGES_PER_ROW * self.page_size)
        end_address   -= end_address   % (self.PAGES_PER_ROW * self.page_size)

        self._clear_page_buffer(samba)

        for offset in xrange(start_address, end_address, self.PAGES_PER_ROW * self.page_size):
            samba.write_word(self.base_address + self.ADDRESS_OFFSET, offset >> 1)

            self._command(samba, self.CMDA_COMMANDS['ER'])
            self._wait_while_busy(samba)


    def program_flash(self, samba, address, data):
        self._get_nvm_params(samba)

        self._clear_page_buffer(samba)

        for offset in xrange(0, len(data), 4):
            word  = data[offset + 0]
            word |= data[offset + 1] << 8
            word |= data[offset + 2] << 16
            word |= data[offset + 3] << 24
            samba.write_word(address + offset, word)

            if offset and offset % self.page_size == 0:
                self._wait_while_busy(samba)

        if (address + len(data)) % self.page_size != 0:
            self._command(samba, self.CMDA_COMMANDS['WP'])

        self._wait_while_busy(samba)


    def verify_flash(self, samba, address, data):
        for offset in xrange(0, len(data), 4):
            word  = data[offset + 0]
            word |= data[offset + 1] << 8
            word |= data[offset + 2] << 16
            word |= data[offset + 3] << 24

            actual_word = samba.read_word(address + offset)
            if actual_word != word:
                return (address + offset, actual_word, word)

        return None
