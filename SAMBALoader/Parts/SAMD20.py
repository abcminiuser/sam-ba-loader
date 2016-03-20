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


class ATSAMD20J18A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 0

@Part.UntestedPart
class ATSAMD20J17A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 1

@Part.UntestedPart
class ATSAMD20J16A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 2

@Part.UntestedPart
class ATSAMD20J15A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 3

@Part.UntestedPart
class ATSAMD20J14A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 4
