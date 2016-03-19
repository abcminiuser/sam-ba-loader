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
import ChipIdentifiers


class Part(object):
    __metaclass__ = abc.ABCMeta


    class __metaclass__(type):
        __inheritors__ = []

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                meta.__inheritors__.append(klass)
            return klass


    @staticmethod
    @abc.abstractmethod
    def get_name():
        pass


    @abc.abstractmethod
    def identify(self, samba):
        pass



class ATSAMD20(Part):
    @staticmethod
    def get_name():
        return "ATSAMD20"


    def identify(self, chip_info):
        return chip_info.processor == 1 and chip_info.family == 0 and chip_info.series == 0



class PartLibrary(object):
    SUPPORTED_PARTS = [c() for c in Part.__inheritors__]


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
