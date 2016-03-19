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


"""Base class for SAM-BA transports. Derived instances should override all methods."""
class Transport(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def read(self):
        pass


    @abc.abstractmethod
    def write(self, data):
        pass
