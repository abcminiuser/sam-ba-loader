#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

from . import Parts
from . import ChipIdentifiers
from . import FlashControllers
import logging


def _get_subclasses(classname):
    """Recursively obtains all subclasses of the given class."""

    subclasses = []

    for p in classname.__subclasses__():
        subclasses.append(p)
        subclasses.extend(_get_subclasses(p))

    return subclasses


class PartLibrary(object):


    """Part library class, which lists all supported devices and provides
       methods to retrieve a given part by its chip identifiers, or by name.
    """

    SUPPORTED_PARTS = _get_subclasses(Parts.PartBase)

    LOG = logging.getLogger(__name__)


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

        # Check if we have a known (named) part architecture (e.g. Cortex-M0+)
        if identifiers['CPUID'].part in identifiers['CPUID'].PART:
            cpuid_part = identifiers['CPUID'].PART[identifiers['CPUID'].part]

            if 'M0' in cpuid_part:
                # Cortex-M0 devices have a DSU for additional information
                identifiers['DSU'] = ChipIdentifiers.DSU(base_address=0x41002000)
                identifiers['DSU'].read(samba)
            else:
                # There are multiple CHIPID locations among various other chips,
                # try them in sequence until we hit one that's likely to be
                # correct
                potential_chipid_addresses = [0x400E0740, 0x400E0940]

                for baseaddress in potential_chipid_addresses:
                    identifiers['CHIPID'] = ChipIdentifiers.CHIPID(base_address=baseaddress)
                    identifiers['CHIPID'].read(samba)

                    # Check if the CHIPID processor type matches the CPUID part
                    if cpuid_part == identifiers['CHIPID'].PROCESSOR[identifiers['CHIPID'].processor]:
                        break

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
