#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Part
from . import CortexM0p


@Part.UntestedPart
class ATSAMC(CortexM0p):
	"""Part class for all SAM C series parts."""

	@staticmethod
	def identify(ids):
		"""Determines if the given chip identifiers positively identify a SAM C
		   series device.

		Args:
			id_name   -- Name of the chip identifier being tested.
			id_values -- Chip identifier values extracted from the part.

		Returns:
			`True` if the given identifiers suggest the part is a SAM C
			series device.
		"""
		try:
			id_values = ids['DSU']
			id_values.processor == 1 and id_values.family == 2 and id_values.series == 1
		except:
			return False
		return True
