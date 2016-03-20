#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import Part
from .. import FlashControllers
import abc


class ATSAMD20(Part.SAMBAPart):
    """Common part implementation for the SAM D20 family devices."""

    FLASH_CONTROLLER   = FlashControllers.NVMCTRL(base_address=0x41004000)

    BOOTLOADER_SIZE    = 2048
    FLASH_BASE_ADDRESS = 0x00000000
    FLASH_APP_ADDRESS  = FLASH_BASE_ADDRESS + BOOTLOADER_SIZE


    def get_name(self):
        """Retrieves the part name as a string. This extracts out the actual
           class name of the sub-classed parts, on the assumption that all
           subclasses of this class will be a specific SAM D20 part (e.g.
           SAMD20J18A).

           Returns:
               Name of the SAM D20 part, as a string.
        """
        return self.__class__.__name__


    def identify(self, id_name, id_values):
        """Determines if a device matches the given ID values that have been
           extracted from the part via a `ChipIdentifier` module. This is a
           common family implementation intended to be sub-classes per-device,
           thus this always returns a failed match.

           Args:
              id_name   : Name of the chip identifier being tested.
              id_values : Chip identifier values extracted from the part.

           Returns:
               `False`.
        """
        return False


    def run_application(self, samba):
        """Runs the application from the start of the device's application area.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        samba.run_from_address(self.FLASH_APP_ADDRESS)


    def erase_chip(self, samba):
        """Erases the device's application area. As the SAM D20 devices do not
           contain a ROM based SAM-BA bootloader, this is massaged into a range
           erase of the flash from the end of the bootloader area to the end of
           the flash.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        self.FLASH_CONTROLLER.erase_flash(samba, start_address=self.FLASH_APP_ADDRESS)


    def program_flash(self, samba, data, address=None):
        """Program's the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              data    : Data to program into the device.
              address : Address to program from (or start of application area
                        if `None`).
        """

        if address is None:
            address = self.FLASH_APP_ADDRESS

        self.FLASH_CONTROLLER.program_flash(samba, address, data)


    def verify_flash(self, samba, data, address=None):
        """Verifies the device's application area against a reference data set.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              data    : Data to verify against.
              address : Address to verify from (or start of application area
                        if `None`).

           Returns:
               `None` if the given data matches the data in the device at the
               specified offset, or a `(address, actual, expected)` tuple of the
               first mismatch.
        """

        if address is None:
            address = self.FLASH_APP_ADDRESS

        return self.FLASH_CONTROLLER.verify_flash(samba, address, data)


    def read_flash(self, samba, address=None, length=None):
        """Reads the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to read from (or start of application area
                        if `None`).
              length  : Length of the data to extract (or until end of
                        application area if `None`).

           Returns:
               Byte array of the extracted data.
        """

        if address is None:
            address = self.FLASH_APP_ADDRESS

        return self.FLASH_CONTROLLER.read_flash(samba, address, length=length)



class ATSAMD20J18A(ATSAMD20):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 0
