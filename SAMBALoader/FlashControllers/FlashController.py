#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import abc


class FlashController(object):
    """Base class for SAM Flash controllers. Derived instances should override
       all methods listed here.
    """

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def erase_flash(self, samba, start_address, end_address=None):
        """Erases the device's application area in the specified region.

           Args:
              samba         : Core `SAMBA` instance bound to the device.
              start_address : Start address to erase.
              end_address   : End address to erase (or end of application area
                              if `None`).
        """
        pass


    @abc.abstractmethod
    def program_flash(self, samba, address, data):
        """Program's the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              address : Address to program from.
              data    : Data to program into the device.
        """
        pass


    @abc.abstractmethod
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
        pass


    @abc.abstractmethod
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
        pass
