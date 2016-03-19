#!/usr/bin/python

#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import SAMBALoader


if __name__=="__main__":
    transport = SAMBALoader.SerialTransport(port='COM3', log_to_console=True)

    samba = SAMBALoader.SAMBA(transport)

    print "SAMBA Version: %s" % samba.get_version()

    print samba.read_word()
