#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import Parts
import ChipIdentifiers
import FlashControllers


class PartLibrary(object):
    """Part library class, which lists all supported devices and provides
       methods to retrieve a given part by its chip identifiers, or by name.
    """

    SUPPORTED_PARTS = [c for c in Parts.PartBase.__inheritors__]


    @staticmethod
    def get_chip_ids(samba):
        """Reads out the chip identifiers from the attached device. Note that
           each device usually implements only a single one of the chip
           identifier modules, thus all but one value will essentially read as
           garbage.

           Args:
               samba : Core `SAMBA` instance bound to the device.

           Returns:
               Dictionary of `{name, identifiers}` for each chip identifier,
               which can then be used to match against a device.
        """
        identifiers = dict()

        identifiers['CPUID'] = ChipIdentifiers.CPUID(base_address=0xE000ED00)
        identifiers['CPUID'].read(samba)

        if identifiers['CPUID'].part in identifiers['CPUID'].PART:
            # Cortex-M0 devices have a DSU for additional information, others use a CHIPID
            if "M0" in identifiers['CPUID'].PART[identifiers['CPUID'].part]:
                identifiers['DSU'] = ChipIdentifiers.DSU(base_address=0x41002000)
                identifiers['DSU'].read(samba)
            else:
                identifiers['CHIPID'] = ChipIdentifiers.CHIPID(base_address=0x400E0940)
                identifiers['CHIPID'].read(samba)

        return identifiers


    @staticmethod
    def find_by_name(name):
        """Retrieves a supported device by its name.

           Args:
              name : Name of the device to retrieve

           Returns:
              List of all parts whose name contains the search string.
        """
        return [p for p in PartLibrary.SUPPORTED_PARTS if p.get_name() == name]


    @staticmethod
    def find_by_chip_ids(chip_ids):
        """Retrieves a supported device by its chip identifiers.

           Args:
              chip_ids : Dictionary of `{name, identifiers}` for each chip
                         identifier that should be matched against all supported
                         devices.

           Returns:
              List of all parts which match against the chip identifiers.
        """
        return [p for p in PartLibrary.SUPPORTED_PARTS for id_name, id_values in chip_ids.items() if p.identify(id_name, id_values)]
