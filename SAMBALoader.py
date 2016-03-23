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
import sys


if __name__ == "__main__":
    transport = SAMBALoader.Transports.Serial(port='COM3', log_to_console=False)

    try:
        samba    = SAMBALoader.SAMBA(transport)
        parts    = SAMBALoader.PartLibrary
        chip_ids = parts.get_chip_ids(samba)
        part     = parts.find_by_chip_ids(chip_ids)

        print 'SAMBA Version: %s' % samba.get_version()
        print '\n'.join('%s Identifiers: %s' % (k, v) for k, v in chip_ids.items())

        if len(part) == 0:
            print 'Error: Unknown part.'
            sys.exit(1)
        elif len(part) > 1:
            print 'Error: Multiple matching parts: %s' % [p.get_name() for p in part]
            sys.exit(1)
        else:
            part = part[0]()

        print 'Discovered Part: %s' % part.get_name()
        if not part.is_tested():
            print "Warning: selected part is currently untested."

        filename = 'LED_TOGGLE_D20_XPRO.bin'
        file_format_processor = SAMBALoader.FileFormatLibrary.find_by_name(filename)

        if len(file_format_processor) == 0:
            print 'Error: No file format reader found.'
        elif len(file_format_processor) > 1:
            print 'Error: Multiple file format readers found.'
        else:
            file_format_processor = file_format_processor[0]()

        bin_data = file_format_processor.read(filename)

        print "Programming flash..."
        part.program_flash(samba, data=bin_data)

        print "Verifying flash..."
        verify_failure = part.verify_flash(samba, data=bin_data)
        if not verify_failure is None:
            print "ERROR: Verification failure @ 0x%08x: 0x%08x != 0x%08x" % verify_failure
            sys.exit(1)

        part.run_application(samba)
    except SAMBALoader.SerialTimeoutError:
        print "ERROR: Serial timeout while waiting for data."
        sys.exit(1)
