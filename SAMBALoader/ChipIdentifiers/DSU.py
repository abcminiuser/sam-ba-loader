#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import ChipIdentifier


class DSU(ChipIdentifier.ChipIdentifierBase):
	"""DSU chip identifier module, used to read out the chip identification
	   registers of a SAM device that contains a DSU module, and extract out the
	   various fields for later comparison against reference part values.
	"""

	DID_OFFSET = 0x0018

	PROCESSOR = {
		0 : "Cortex-M0",
		1 : "Cortex-M0+",
		2 : "Cortex-M3",
		3 : "Cortex-M4",
	}
	FAMILY = {
		0 : "SAM D",
		1 : "SAM L",
		2 : "SAM C",
	}


	def __init__(self, base_address):
		"""Initializes a DSU chip identifier instance at the specified base
		   address in the attached device.

		Args:
			base_address -- Base address of the DSU module within the internal
							address space of the attached device.
		"""

		self.base_address = base_address


	def __str__(self):
		"""Conversion method to serialize the parsed chip identifier values out
		   as a string.

		Returns:
			Chip identifier values as a human readable string suitable for
			printing to a console.
		"""

		info  = "\n\tProcessor:\t" + self._lookup(self.PROCESSOR, self.processor)
		info += "\n\tFamily:\t\t" + self._lookup(self.FAMILY, self.family)
		info += "\n\tSeries:\t\t" + str(self.series)
		info += "\n\tDie:\t\t" + str(self.die)
		info += "\n\tRevision:\t" + str(self.revision)
		info += "\n\tVariant:\t" + str(self.variant)

		return info


	def _lookup(self, table, value):
		"""Internal lookup helper function, searching a lookup table for the
		   specified value, or returning the raw value and an unknown identifier
		   warning.

		Args:
			table -- Lookup table to examine.
			value -- Value to search for in the table.

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
			samba -- Core `SAMBA` instance bound to the device.
		"""

		self.chip_id = samba.read_word(self.base_address + self.DID_OFFSET)
		if self.chip_id == 0:
			return False

		self.processor = (self.chip_id >> 28) & 0x000F
		self.family    = (self.chip_id >> 23) & 0x001F
		self.series    = (self.chip_id >> 16) & 0x003F
		self.die       = (self.chip_id >> 12) & 0x000F
		self.revision  = (self.chip_id >>  8) & 0x000F
		self.variant   = (self.chip_id >>  0) & 0x00FF
		return True
