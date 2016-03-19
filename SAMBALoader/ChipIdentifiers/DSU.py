#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.


class DSU(object):
    CHIP_ID_OFFSET = 0x0018


    def __init__(self, base_address):
        self.base_address = base_address


    def read(self, samba):
        chip_id = samba.read_word(self.base_address + self.CHIP_ID_OFFSET)

        processor = (chip_id >> 28) & 0x000F
        family    = (chip_id >> 23) & 0x001F
        series    = (chip_id >> 16) & 0x003F
        die       = (chip_id >> 12) & 0x000F
        revision  = (chip_id >>  8) & 0x000F
        variant   = (chip_id >>  0) & 0x00FF

        return DSUIdentifier(processor, family, series, die, revision, variant)



class DSUIdentifier(object):
    PROCESSOR = {
        1 : "CORTEX M0+"
    }
    FAMILY = {
        0 : "SAM D"
    }
    SERIES = {
        0 : "CORTEX M0+ Basic Feature Set"
    }


    def _lookup(self, table, value):
        return table[value] if value in table else '?'


    def __str__(self):
        info  = "\n\tProcessor:\t" + self._lookup(self.PROCESSOR, self.processor)
        info += "\n\tFamily:\t\t" + self._lookup(self.FAMILY, self.family)
        info += "\n\tSeries:\t\t" + self._lookup(self.SERIES, self.series)
        info += "\n\tDie:\t\t" + str(self.die)
        info += "\n\tRevision:\t" + str(self.revision)
        info += "\n\tVariant:\t" + str(self.variant)

        return info


    def __init__(self, processor, family, series, die, revision, variant):
        self.processor = processor
        self.family    = family
        self.series    = series
        self.die       = die
        self.revision  = revision
        self.variant   = variant
