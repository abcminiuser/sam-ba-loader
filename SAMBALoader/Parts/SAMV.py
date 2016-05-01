#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

from . import Part
from . import CortexM7


class ATSAMV(CortexM7):
    """Part class for all SAM E/S/V series parts."""

    @staticmethod
    def identify(id_name, id_values):
        """Determines if the given chip identifiers positively identify a
           SAM E/S/V series device.

           Args:
              id_name   : Name of the chip identifier being tested.
              id_values : Chip identifier values extracted from the part.

           Returns:
               `True` if the given identifiers suggest the part is a SAM E/S/V
               series device.
        """
        return id_name == 'CHIPID' and id_values.processor == 0 and id_values.architecture == 1
