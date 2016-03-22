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


@Part.UntestedPart
class ATSAMC(CortexM0p.CortexM0p):
    """Part class for all SAM C series parts."""

    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 2 and id_values.series == 1
