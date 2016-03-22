#
#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

import Part
import CortexM0p


class ATSAMD20(CortexM0p.CortexM0p):
    """Base class for all ATSAM D20 based parts. Specific parts should extend
       this base class, setting their variant ID as appropriate.\
    """

    VARIANT = None

    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == self.VARIANT



class ATSAMD20J18A(ATSAMD20):
    VARIANT = 0

@Part.UntestedPart
class ATSAMD20J17A(ATSAMD20):
    VARIANT = 1

@Part.UntestedPart
class ATSAMD20J16A(ATSAMD20):
    VARIANT = 2

@Part.UntestedPart
class ATSAMD20J15A(ATSAMD20):
    VARIANT = 3

@Part.UntestedPart
class ATSAMD20J14A(ATSAMD20):
    VARIANT = 4

@Part.UntestedPart
class ATSAMD20G18A(ATSAMD20):
    VARIANT = 5

@Part.UntestedPart
class ATSAMD20G17A(ATSAMD20):
    VARIANT = 6

@Part.UntestedPart
class ATSAMD20G16A(ATSAMD20):
    VARIANT = 7

@Part.UntestedPart
class ATSAMD20G15A(ATSAMD20):
    VARIANT = 8

@Part.UntestedPart
class ATSAMD20G14A(ATSAMD20):
    VARIANT = 9

@Part.UntestedPart
class ATSAMD2E18A(ATSAMD20):
    VARIANT = 10

@Part.UntestedPart
class ATSAMD20E17A(ATSAMD20):
    VARIANT = 11

@Part.UntestedPart
class ATSAMD20E16A(ATSAMD20):
    VARIANT = 12

@Part.UntestedPart
class ATSAMD20E15A(ATSAMD20):
    VARIANT = 13

@Part.UntestedPart
class ATSAMD20E14A(ATSAMD20):
    VARIANT = 14
