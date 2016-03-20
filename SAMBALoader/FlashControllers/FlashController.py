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


class FlashController(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def erase_flash(self, samba, start_address=None, end_address=None):
        pass


    @abc.abstractmethod
    def program_flash(self, samba, address, data):
        pass


    @abc.abstractmethod
    def verify_flash(self, samba, address, data):
        pass


    @abc.abstractmethod
    def read_flash(self, samba, address, length=None):
        pass
