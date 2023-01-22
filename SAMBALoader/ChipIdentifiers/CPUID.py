#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import ChipIdentifier


class CPUID(ChipIdentifier.ChipIdentifierBase):
	"""CPUID chip identifier module, used to read out the ARM core
	   identification register from an unknown ARM device, and extract out the
	   various fields for later comparison against reference part values.
	"""

	IMPLEMENTER = {
		0x41 : "ARM",
	}

	ARCHITECTURE = {
		0xC : "ARMv6-M",
		0xF : "ARMv7-M",
	}

	PART = {
		0xC20 : "Cortex-M0",
		0xC21 : "Cortex-M1",
		0xC23 : "Cortex-M3",
		0xC24 : "Cortex-M3/Cortex-M4",
		0xC27 : "Cortex-M7",
		0xC60 : "Cortex-M0+",
	}


	def __init__(self, base_address):
		"""Initializes a CPUID chip identifier instance at the specified base
		   address in the attached device.

		Args:
			base_address -- Base address of the CPUID module within the
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

		ret = 'CPUID @ 0x{:08X}: 0x{:08X}'.format(self.base_address, self.chip_id)
		ret += "\n\tImplementer:\t" + self._lookup(self.IMPLEMENTER, self.implementer)
		ret += "\n\tArchitecture:\t" + self._lookup(self.ARCHITECTURE, self.architecture)
		ret += "\n\tVersion:\t" + "r%dp%d" % (self.variant, self.revision)
		ret += "\n\tPart:\t\t" + self._lookup(self.PART, self.part)
		return ret


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
		"""Reads and parses the CPU identification values from the attached
		   device. Parsed values are then stored in the class instance, and can
		   be extracted later for matching against a specific device.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""

		self.chip_id = samba.read_word(self.base_address)
		if self.chip_id == 0:
			return False

		self.implementer  = (self.chip_id >> 24) & 0x0000FF
		self.variant      = (self.chip_id >> 20) & 0x00000F
		self.architecture = (self.chip_id >> 16) & 0x00000F
		self.part         = (self.chip_id >> 4)  & 0x000FFF
		self.revision     = (self.chip_id >> 0)  & 0x00000F
		return True
