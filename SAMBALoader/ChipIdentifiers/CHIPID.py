#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from .import ChipIdentifier


class CHIPID(ChipIdentifier.ChipIdentifierBase):
	"""CHIPID chip identifier module, used to read out the chip identification
	   registers of a SAM device that contains a CHIPID module, and extract out
	   the various fields for later comparison against reference part values.
	"""

	CIDR_OFFSET = 0x0000
	EXID_OFFSET = 0x0004

	FLASH_BANK_SIZE = {
		0  : 'NONE',
		1  : '8KB',
		2  : '16KB',
		3  : '32KB',
		5  : '64KB',
		7  : '128KB',
		9  : '256KB',
		10 : '512KB',
		12 : '1024KB',
		14 : '2048KB',
	}

	SRAM_SIZE = {
		0  : '48KB',
		1  : '1KB',
		2  : '2KB',
		3  : '6KB',
		4  : '24KB',
		5  : '4KB',
		6  : '80KB',
		7  : '160KB',
		8  : '8KB',
		9  : '16KB',
		10 : '32KB',
		11 : '64KB',
		12 : '128KB',
		13 : '256KB',
		14 : '96KB',
		15 : '512KB',
	}

	PROCESSOR = {
		0  : 'Cortex-M7',
		1  : 'ARM946ES',
		2  : 'ARM7TDMI',
		3  : 'Cortex-M3',
		4  : 'ARM920T',
		5  : 'ARM926EJS',
		6  : 'Cortex-A5',
		7  : 'Cortex-M4',
	}

	ARCHITECTURE = {
		0x19 : 'AT91SAM9xx Series',
		0x29 : 'AT91SAM9XExx Series',
		0x34 : 'AT91x34 Series',
		0x37 : 'CAP7 Series',
		0x39 : 'CAP9 Series',
		0x3B : 'CAP11 Series',
		0x40 : 'AT91x40 Series',
		0x42 : 'AT91x42 Series',
		0x55 : 'AT91x55 Series',
		0x60 : 'AT91SAM7Axx Series',
		0x61 : 'AT91SAM7AQxx Series',
		0x63 : 'AT91x63 Series',
		0x70 : 'AT91SAM7Sxx Series',
		0x71 : 'AT91SAM7XCxx Series',
		0x72 : 'AT91SAM7SExx Series',
		0x73 : 'AT91SAM7Lxx Series',
		0x75 : 'AT91SAM7Xxx Series',
		0x76 : 'AT91SAM7SLxx Series',
		0x80 : 'SAM3UxC Series (100-pin version)',
		0x81 : 'SAM3UxE Series (144-pin version)',
		0x83 : 'SAM3AxC Series (100-pin version)',
		0x84 : 'SAM3XxC Series (100-pin version)',
		0x85 : 'SAM3XxE Series (144-pin version)',
		0x86 : 'SAM3XxG Series (217-pin version)',
		0x88 : 'SAM4SxA (48-pin version)',
		0x89 : 'SAM4SxB (64-pin version)',
		0x8A : 'SAM4SxC (100-pin version)',
		0x92 : 'AT91x92 Series',
		0x93 : 'SAM3NxA Series (48-pin version)',
		0x94 : 'SAM3NxB Series (64-pin version)',
		0x95 : 'SAM3NxC Series (100-pin version)',
		0x98 : 'SAM4SDxA Series (48-pin version)',
		0x99 : 'SAM4SDxB Series (64-pin version)',
		0x9A : 'SAM4SDxC Series (100-pin version)',
		0xA5 : 'SAM5A',
		0xF0 : 'AT75Cxx Series',
	}


	def __init__(self, base_address):
		"""Initializes a CHIPID chip identifier instance at the specified base
		   address in the attached device.

		Args:
			base_address -- Base address of the CHIPID module within the
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

		ret = 'CHIPID @ 0x{:08X}: 0x{:08X}'.format(self.base_address, self.chip_id)
		ret += '\n\tVersion:\t' + str(self.version)
		ret += '\n\tProcessor:\t' + self._lookup(self.PROCESSOR, self.processor)
		ret += '\n\tArchitecture:\t' + self._lookup(self.ARCHITECTURE, self.architecture)
		ret += '\n\tFlash Bank 0:\t' + self._lookup(self.FLASH_BANK_SIZE, self.flash[0])
		ret += '\n\tFlash Bank 1:\t' + self._lookup(self.FLASH_BANK_SIZE, self.flash[1])
		ret += '\n\tSRAM:\t\t' + self._lookup(self.SRAM_SIZE, self.sram)
		ret += '\n\tExtended ID:\t' + str(self.extended_chip_id)
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

		return table[value] if value in table else '{0} (0x{0:X}) (Unknown)'.format(value)


	def read(self, samba):
		"""Reads and parses the chip identification values from the attached
		   device. Parsed values are then stored in the class instance, and can
		   be extracted later for matching against a specific device.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""

		self.chip_id = samba.read_word(self.base_address + self.CIDR_OFFSET)
		if self.chip_id == 0:
			return False
		self.extended_chip_id = samba.read_word(self.base_address + self.EXID_OFFSET)

		self.version      = (self.chip_id >> 0)  & 0x00001F
		self.processor    = (self.chip_id >> 5)  & 0x000007
		self.flash        = [(self.chip_id >> 8) & 0x00000F, (self.chip_id >> 12) & 0x00000F]
		self.sram         = (self.chip_id >> 16) & 0x00000F
		self.architecture = (self.chip_id >> 20) & 0x0000FF
		return True
