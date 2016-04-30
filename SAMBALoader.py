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
import SAMBALoader.Transports
import sys
import logging



class SessionError(Exception):
    pass



class Session(object):

    def __init__(self, samba):
        self.samba = samba
        self.part  = None


    def _get_part(self, chip_ids):
        matched_parts = SAMBALoader.PartLibrary.find_by_chip_ids(chip_ids)

        if len(matched_parts) == 0:
            raise SessionError('Unknown part.')
        elif len(matched_parts) > 1:
            raise SessionError('Multiple matching parts: %s' % [p.get_name() for p in matched_parts])
        else:
            return matched_parts[0]()


    def _get_file_processor(self, filename):
        matched_formats = SAMBALoader.FileFormatLibrary.find_by_name(filename)

        if len(matched_formats) == 0:
            raise SessionError('Unknown file format: %s' % filename)
        elif len(matched_formats) > 1:
            raise SessionError('Multiple matching file formats: %s' % [f.get_name() for f in matched_formats])
        else:
            return matched_formats[0]()


    def get_part_identifiers(self):
        return SAMBALoader.PartLibrary.get_chip_ids(self.samba)


    def set_part_by_chip_ids(self, chip_ids):
        self.part = self._get_part(chip_ids)

        return self.part


    def program_flash(self, filename):
        if self.part is None:
            raise SessionError('Part not set.')

        file_format = self._get_file_processor(filename)
        file_data   = file_format.read(filename)

        self.part.program_flash(self.samba, data=file_data)


    def verify_flash(self, filename):
        if self.part is None:
            raise SessionError('Part not set.')

        file_format = self._get_file_processor(filename)
        file_data   = file_format.read(filename)

        verify_failure = self.part.verify_flash(self.samba, data=file_data)
        if verify_failure is not None:
            raise SessionError('Verification failure @ 0x%08x: 0x%08x != 0x%08x' % verify_failure)



if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    if len(sys.argv) != 3:
        print("Atmel SAM-BA Client")
        print("\tUsage: %s [PORT] [FILENAME]" % sys.argv[0])
        sys.exit(1)

    serial_device       = sys.argv[1]
    filename_to_program = sys.argv[2]

    try:
        transport = SAMBALoader.Transports.Serial(port=serial_device)
        samba     = SAMBALoader.SAMBA(transport, is_usb=False)
        session   = Session(samba)

        print('SAMBA Version: %s' % samba.get_version())

        chip_ids = session.get_part_identifiers()
        print('\n'.join('%s Identifiers: %s' % (k, v) for k, v in chip_ids.items()))

        part = session.set_part_by_chip_ids(chip_ids)
        print('Discovered Part: %s' % part.get_name())
        if not part.is_tested():
            print('WARNING: selected part is currently untested.')

        print('Programming flash...')
        session.program_flash(filename_to_program)

        print('Verifying flash...')
        session.verify_flash(filename_to_program)

        print('Done, booting to application.')
        part.run_application(samba)

    except SAMBALoader.Transports.TimeoutError:
        print('ERROR: Timeout while waiting for data.')
        sys.exit(1)

    except SessionError as e:
        print('ERROR: ' + str(e))
        sys.exit(1)
