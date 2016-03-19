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

class ATSAMD20J18A(Part.SAMBAPart):
    @staticmethod
    def get_name():
        return "ATSAMD20J18A"


    def identify(self, chip_info):
        return chip_info.processor == 1 and chip_info.family == 0 and chip_info.series == 0 and chip_info.variant == 0
