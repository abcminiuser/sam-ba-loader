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


class EFC(FlashController.FlashControllerBase):

    def __init__(self, base_address):
        """Initializes a EFC controller instance at the specified base
           address in the attached device.

           Args:
               base_address : Base address of the EFC module within the
                              internal address space of the attached device
        """

        self.base_address = base_address


    def _get_nvm_params(self, samba):
        """Retrieves the NVM parameters from the attached device, and caches
           then in the class instance.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """

        pass


    def _wait_while_busy(self, samba):
        """Waits until the NVM controller in the attached device is ready for a
           new operation.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """

        pass


    def _command(self, samba, command):
        """Issues a low-level command to the NVMCTRL module within the
            connected device.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              command : Command value to issue (see `CTRLA_CMDA`)
        """

        pass


    def erase_flash(self, samba, start_address, end_address=None):
        """Erases the device's application area in the specified region.

           Args:
              samba         : Core `SAMBA` instance bound to the device.
              start_address : Start address to erase.
              end_address   : End address to erase (or end of application area
                              if `None`).
        """

        pass


    def program_flash(self, samba, address, data):
        """Program's the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to program from.
              data    : Data to program into the device.
        """

        pass


    def verify_flash(self, samba, address, data):
        """Verifies the device's application area against a reference data set.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to verify from.
              data    : Data to verify against.

           Returns:
               `None` if the given data matches the data in the device at the
               specified offset, or a `(address, actual_word, expected_word)`
               tuple of the first mismatch.
        """

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

        return None
