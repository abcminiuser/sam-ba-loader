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


class PartBase(object):
    """Base class for supported SAM-BA devices. Derived instances should
       override all methods listed here.
    """

    __metaclass__ = abc.ABCMeta


    PART_UNTESTED = False


    class __metaclass__(type):
        """Metaclass instantiation, which tracks all classes which extend this
           base class. This is used to automatically inject all objects which
           derive from this interface into the part library, so that they are
           automatically supported.
        """
        __inheritors__ = []

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                if not klass in meta.__inheritors__:
                    meta.__inheritors__.append(klass)
            return klass


    def is_tested(self):
        """Determines if the current part has been tested (if not, a warning
           message should be displayed).

           Returns:
               `True` if the part has been physically verified as working,
               `False` otherwise.
        """
        return not self.PART_UNTESTED


    @abc.abstractmethod
    def get_name(self):
        """Device name, as a short string that can be displayed to the user or
           matched against a requested device name.

           Returns:
               Name of the device, as a string.
        """
        pass


    @staticmethod
    @abc.abstractmethod
    def identify(id_name, id_values):
        """Determines if a device matches the given ID values that have been
           extracted from the part via a `ChipIdentifier` module.

           Args:
              id_name   : Name of the chip identifier being tested.
              id_values : Chip identifier values extracted from the part.

           Returns:
               `True` if the part matches the given identifier.
        """
        pass


    @abc.abstractmethod
    def run_application(self, samba):
        """Runs the application from the start of the device's application area.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        pass


    @abc.abstractmethod
    def erase_chip(self, samba):
        """Erases the device's application area.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        pass


    @abc.abstractmethod
    def program_flash(self, samba, data, address=None):
        """Program's the device's application area.

           Args:
              samba   : Core `SAMBA` instance bound to the device.
              data    : Data to program into the device.
              address : Address to program from (or start of application area
                        if `None`).
        """
        pass


    @abc.abstractmethod
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
        pass


    @abc.abstractmethod
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
        pass


def UntestedPart(part):
    """Decorator applied to parts who have not yet been physically tested to
       ensure they work as expected.
    """
    part.PART_UNTESTED = True
