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
    SUPPORTED_PARTS = [c() for c in Parts.SAMBAPart.__inheritors__]


    @staticmethod
    def get_chip_identifiers(samba):
        identifiers = dict()

        identifiers['DSU'] = ChipIdentifiers.DSU(base_address=0x41002000).read(samba)

        return identifiers


    @staticmethod
    def find_by_name(name):
        return [p for p in PartLibrary.SUPPORTED_PARTS if p.get_name() == name]


    @staticmethod
    def find_by_chip_id(chip_ids):
        return [p for p in PartLibrary.SUPPORTED_PARTS for i in chip_ids if p.identify(i)]
