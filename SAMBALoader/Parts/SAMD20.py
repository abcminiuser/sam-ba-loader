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

@Part.UntestedPart
class ATSAMD20G18A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 5

@Part.UntestedPart
class ATSAMD20G17A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 6

@Part.UntestedPart
class ATSAMD20G16A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 7

@Part.UntestedPart
class ATSAMD20G15A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 8

@Part.UntestedPart
class ATSAMD20G14A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 9

@Part.UntestedPart
class ATSAMD2E18A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 10

@Part.UntestedPart
class ATSAMD20E17A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 11

@Part.UntestedPart
class ATSAMD20E16A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 12

@Part.UntestedPart
class ATSAMD20E15A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 13

@Part.UntestedPart
class ATSAMD20E14A(CortexM0p.CortexM0p):
    def identify(self, id_name, id_values):
        return id_name == "DSU" and id_values.processor == 1 and id_values.family == 0 and id_values.series == 0 and id_values.variant == 14
