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
    FLASH_CONTROLLER   = FlashControllers.NVMCTRL(base_address=0x41004000)

    FLASH_BASE_ADDRESS = 0x00000000
    BOOTLOADER_SIZE    = 0x40000


    @staticmethod
    def get_name():
        return "ATSAMD20J18A"


    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 0


    def run_application(self, samba):
        samba.run_from_address(self.FLASH_BASE_ADDRESS + self.BOOTLOADER_SIZE)


    def erase_chip(self, samba):
        self.FLASH_CONTROLLER.erase_chip(samba)


    def program_flash(self, samba, data, address=None):
        if address is None:
            address = self.FLASH_BASE_ADDRESS + self.BOOTLOADER_SIZE

        self.FLASH_CONTROLLER.program_flash(samba, address, data)
