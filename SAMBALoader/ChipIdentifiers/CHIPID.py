#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import ChipIdentifier


class CHIPID(ChipIdentifier.ChipIdentifier):
    """CHIPID chip identifier module, used to read out the chip identification
       registers of a SAM device that contains a CHIPID module, and extract out
       the various fields for later comparison against reference part values.
    """

    CIDR_OFFSET = 0x0000
    EXID_OFFSET = 0x0004

    FLASH_BANK_SIZE = {
        0  : "NONE",
        1  : "8KB",
        2  : "16KB",
        3  : "32KB",
        5  : "64KB",
        7  : "128KB",
        9  : "256KB",
        10 : "512KB",
        12 : "1024KB",
        14 : "2048KB",
    }

    SRAM_SIZE = {
        0  : "48KB",
        1  : "1KB",
        2  : "2KB",
        3  : "6KB",
        4  : "24KB",
        5  : "4KB",
        6  : "80KB",
        7  : "160KB",
        8  : "8KB",
        9  : "16KB",
        10 : "32KB",
        11 : "64KB",
        12 : "128KB",
        13 : "256KB",
        14 : "96KB",
        15 : "512KB",
    }

    PROCESSOR = {
        0  : "Cortex-M7",
        1  : "ARM946ES",
        2  : "ARM7TDMI",
        3  : "Cortex-M3",
        4  : "ARM920T",
        5  : "ARM926EJS",
        6  : "Cortex-A5",
        7  : "Cortex-M4",
    }


    def __init__(self, base_address):
        """Initializes a CHIPID chip identifier instance at the specified base
           address in the attached device.

           Args:
               base_address : Base address of the CHIPID module within the
                              internal address space of the attached device.
        """

        self.base_address = base_address


    def __str__(self):
        """Conversion method to serialize the parsed chip identifier values out
           as a string.

           Returns:
               Chip identifier values as a human readable string suitable for
               printing to a console.
        """

        info  = "\n\tVersion:\t" + str(self.version)
        info += "\n\tProcessor:\t" + self._lookup(self.PROCESSOR, self.processor)
        info += "\n\tArchitecture:\t" + str(self.architecture)
        info += "\n\tFlash Bank 0:\t" + self._lookup(self.FLASH_BANK_SIZE, self.flash[0])
        info += "\n\tFlash Bank 1:\t" + self._lookup(self.FLASH_BANK_SIZE, self.flash[1])
        info += "\n\tSRAM:\t\t" + self._lookup(self.SRAM_SIZE, self.sram)
        info += "\n\tExtended ID:\t" + str(self.extended_chip_id)

        return info


    def _lookup(self, table, value):
        """Internal lookup helper function, searching a lookup table for the
           specified value, or returning the raw value and an unknown identifier
           warning.

           Args:
               table : Lookup table to examine.
               value : Value to search for in the table.

           Returns:
               String matching the value in the table if found, or the raw value
               (as a string) if not.
        """

        return table[value] if value in table else '%d (Unknown)' % value


    def read(self, samba):
        """Reads and parses the chip identification values from the attached
           device. Parsed values are then stored in the class instance, and can
           be extracted later for matching against a specific device.

           Args:
              samba : Core `SAMBA` instance bound to the device.
        """

        self.chip_id = samba.read_word(self.base_address + self.CIDR_OFFSET)
        self.extended_chip_id = samba.read_word(self.base_address + self.EXID_OFFSET)

        self.version      = (self.chip_id >> 0)  & 0x00000F
        self.processor    = (self.chip_id >> 5)  & 0x000007
        self.flash        = [(self.chip_id >> 8) & 0x00000F, (self.chip_id >> 12) & 0x00000F]
        self.sram         = (self.chip_id >> 16) & 0x00000F
        self.architecture = (self.chip_id >> 24) & 0x00000F
