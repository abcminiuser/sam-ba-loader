#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Part
from . import CortexM0p


class ATSAMD(CortexM0p):
	"""Part class for all SAM D based parts."""

	@staticmethod
	def identify(idS):
		"""Determines if the given chip identifiers positively identify a SAM D
		   series device.

		Args:
			id_name   -- Name of the chip identifier being tested.
			id_values -- Chip identifier values extracted from the part.

		Returns:
			`True` if the given identifiers suggest the part is a SAM D
			series device.
		"""
		try:
			id_values = ids['DSU']
			id_values.processor == 1 and id_values.family == 0 and id_values.series == 0
		except:
			return False
		return True
