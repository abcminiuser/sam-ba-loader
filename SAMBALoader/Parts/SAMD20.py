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


class ATSAMD20J18A(Part.SAMBAPart):
    FLASH_CONTROLLER = FlashControllers.NVMCTRL(base_address=0x41004000)


    @staticmethod
    def get_name():
        return "ATSAMD20J18A"


    def identify(self, chip_info):
        return chip_info.processor == 1 and chip_info.family == 0 and chip_info.series == 0 and chip_info.variant == 0


    def erase_chip(self, samba):
        self.FLASH_CONTROLLER.erase_chip(samba)
