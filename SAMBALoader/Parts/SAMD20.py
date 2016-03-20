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
    FLASH_CONTROLLER   = FlashControllers.NVMCTRL(base_address=0x41004000)

    BOOTLOADER_SIZE    = 2048
    FLASH_BASE_ADDRESS = 0x00000000
    FLASH_APP_ADDRESS  = FLASH_BASE_ADDRESS + BOOTLOADER_SIZE


    def get_name(self):
        return self.__class__.__name__


    def run_application(self, samba):
        samba.run_from_address(self.FLASH_APP_ADDRESS)


    def erase_chip(self, samba):
        self.FLASH_CONTROLLER.erase_flash(samba, start_address=self.FLASH_APP_ADDRESS)


    def program_flash(self, samba, data, address=None):
        if address is None:
            address = self.FLASH_APP_ADDRESS

        self.FLASH_CONTROLLER.program_flash(samba, address, data)


    def verify_flash(self, samba, data, address=None):
        if address is None:
            address = self.FLASH_APP_ADDRESS

        return self.FLASH_CONTROLLER.verify_flash(samba, address, data)


    def read_flash(self, samba, address=None, length=None):
        if address is None:
            address = self.FLASH_APP_ADDRESS

        return self.FLASH_CONTROLLER.read_flash(samba, address, length=length)


    def identify(self, id_name, id_values):
        return False



class ATSAMD20J18A(ATSAMD20):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 0


