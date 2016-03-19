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


class SAMBAPart(object):
    __metaclass__ = abc.ABCMeta


    class __metaclass__(type):
        __inheritors__ = []

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                if not klass in meta.__inheritors__:
                    meta.__inheritors__.append(klass)
            return klass


    @staticmethod
    @abc.abstractmethod
    def get_name():
        pass


    @abc.abstractmethod
    def identify(self, id_name, id_values):
        pass


    @abc.abstractmethod
    def run_application(self, samba):
        pass


    @abc.abstractmethod
    def erase_chip(self, samba):
        pass

