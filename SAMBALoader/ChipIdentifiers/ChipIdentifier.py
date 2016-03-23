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
import logging


class ChipIdentifierBase(object):
    """Base class for SAM chip identification modules. Derived instances should
       override all methods listed here.
    """

    __metaclass__ = abc.ABCMeta

    LOG = logging.getLogger(__name__)


    @abc.abstractmethod
    def read(self, samba):
        """Reads and parses the chip identification values from the attached
           device. Parsed values are then stored in the class instance, and can
           be extracted later for matching against a specific device.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """
        pass
