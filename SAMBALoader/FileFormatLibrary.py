#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import FileFormats
import logging


class FileFormatLibrary(object):
    """Part library class, which lists all supported devices and provides
       methods to retrieve a given part by its chip identifiers, or by name.
    """

    SUPPORTED_FORMATS = [c for c in FileFormats.FileFormatBase.__inheritors__]

    LOG = logging.getLogger(__name__)


    @staticmethod
    def find_by_name(filename):
        """Retrieves a supported file format processor from a filename.

           Args:
              filename : Filename to check against all file processors.

           Returns:
              List of all format processors which match against the filename.
        """
        return [f for f in FileFormatLibrary.SUPPORTED_FORMATS if f.can_process(filename)]
