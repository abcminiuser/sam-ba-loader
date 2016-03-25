#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

from . import FlashController

try:
    xrange
except NameError:
    # Remap xrange to range for Python 3
    xrange = range


class NVMCTRL(FlashController.FlashControllerBase):
    CMDA_OFFSET      = 0x0000
    PARAM_OFFSET     = 0x0008
    STATUS_OFFSET    = 0x0018
    INTFLAG_OFFSET   = 0x0014
    ADDRESS_OFFSET   = 0x001C

    INTFLAG_READY    = (1 << 0)
    INTFLAG_ERROR    = (1 << 1)

    CMDA_COMMANDS    = {
        'ER'  : 0x02,
        'WP'  : 0x04,
        'PBC' : 0x44,
    }

    PAGES_PER_ROW    = 4


    def __init__(self, base_address):
        """Initializes a NVMCTRL controller instance at the specified base
           address in the attached device.

           Args:
               base_address : Base address of the NVMCTRL module within the
                              internal address space of the attached device
        """

        self.base_address = base_address


    def _get_nvm_params(self, samba):
        """Retrieves the NVM parameters from the attached device, and caches
           then in the class instance.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """

        nvm_param = samba.read_word(self.base_address + self.PARAM_OFFSET)

        self.page_size = 8 << ((nvm_param >> 16) & 0x07)
        self.pages     = nvm_param & 0xFFFF


    def _wait_while_busy(self, samba):
        """Waits until the NVM controller in the attached device is ready for a
           new operation.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        while not samba.read_half_word(self.base_address + self.INTFLAG_OFFSET) & self.INTFLAG_READY:
            pass


    def _command(self, samba, command):
        """Issues a low-level command to the NVMCTRL module within the
            connected device.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              command : Command value to issue (see `CMDA_COMMANDS`)
        """

        self._wait_while_busy(samba)

        reg  = (0xA5 << 8) | command
        samba.write_half_word(self.base_address + self.CMDA_OFFSET, reg)


    def erase_flash(self, samba, start_address, end_address=None):
        """Erases the device's application area in the specified region.

           Args:
              samba         : Core `SAMBA` instance bound to the device.
              start_address : Start address to erase.
              end_address   : End address to erase (or end of application area
                              if `None`).
        """

        self._get_nvm_params(samba)

        if end_address is None:
            end_address = self.pages * self.page_size

        start_address -= start_address % (self.PAGES_PER_ROW * self.page_size)
        end_address   -= end_address   % (self.PAGES_PER_ROW * self.page_size)

        for offset in xrange(start_address, end_address, self.PAGES_PER_ROW * self.page_size):
            samba.write_word(self.base_address + self.ADDRESS_OFFSET, offset >> 1)

            self._command(samba, self.CMDA_COMMANDS['ER'])
            self._wait_while_busy(samba)


    def program_flash(self, samba, address, data):
        """Program's the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to program from.
              data    : Data to program into the device.
        """

        self._get_nvm_params(samba)

        self._command(samba, self.CMDA_COMMANDS['PBC'])
        self._wait_while_busy(samba)

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
        """Verifies the device's application area against a reference data set.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to verify from.
              data    : Data to verify against.

           Returns:
               `None` if the given data matches the data in the device at the
               specified offset, or a `(address, actual, expected)` tuple of the
               first mismatch.
        """

        for offset in xrange(0, len(data), 4):
            word  = data[offset + 0]
            word |= data[offset + 1] << 8
            word |= data[offset + 2] << 16
            word |= data[offset + 3] << 24

            actual_word = samba.read_word(address + offset)
            if actual_word != word:
                return (address + offset, actual_word, word)

        return None


    def read_flash(self, samba, address, length=None):
        """Reads the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to read from.
              length  : Length of the data to extract (or until end of
                        application area if `None`).

           Returns:
               Byte array of the extracted data.
        """

        self._get_nvm_params(samba)

        if length is None:
            length = (self.pages * self.page_size) - address

        data = []

        for offset in xrange(0, length, 4):
            word = samba.read_word(address + offset)

            data.append(word >> 0  & 0xFF)
            data.append(word >> 8  & 0xFF)
            data.append(word >> 16 & 0xFF)
            data.append(word >> 24 & 0xFF)

        return data
