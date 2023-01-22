#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Part
from . import CortexM3_4
from ..FlashControllers import EEFCFlash, AddressRange
from ..Peripheral import RSTC


class SAM3X(CortexM3_4):
	"""Base part class for SAM3A and SAM3X series."""


	def __init__(self, samba, flash_planes, flash_total_length):
		"""Initializes class with flash & RSTC

		Args:
			flash_planes       -- flash planes & controllers count: 1 or 2
			flash_total_length -- total flash length, kBytes
		"""
		CortexM3_4.__init__(self, samba)
		self.flash_address_range = AddressRange(0x00080000, flash_total_length * 1024, int((flash_total_length * 1024) // flash_planes))
		if flash_planes == 1:
			self.flash_controllers = (
				EEFCFlash.Flash(self.samba, 0x00080000, 0x400E0A00, flash_total_length * 4, 256, dont_use_read_block=True),
				)
		else:
			self.flash_controllers = (
				EEFCFlash.Flash(self.samba, 0x00080000, 0x400E0A00, flash_total_length * 2, 256, dont_use_read_block=True),
				EEFCFlash.Flash(self.samba, 0x00080000 + flash_total_length * 512, 0x400E0C00, flash_total_length * 2, 256, dont_use_read_block=True),
				)
		self.reset_controller = RSTC(samba, 0x400E1A00)


	@classmethod
	def identify(cls, ids):
		if not hasattr(cls, 'CHIP_ID'):
			return False
		try:
			chip_id = ids['CHIPID'].chip_id & 0x7FFFFFE0 # remove revision (A)
		except:
			return False
		return chip_id == cls.CHIP_ID


	@classmethod
	def get_name(cls):
		"""Retrieves the part name as a string. This extracts out the actual
		   class name of the sub-classed parts.

		Returns:
			Name of the SAM part, as a string (empty string for base classes).
		"""
		return '' if cls is SAM3X else cls.__name__


@Part.UntestedPart
class ATSAM3X8H(SAM3X):
	CHIP_ID = 0x286E0A60
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 256)


class ATSAM3X8E(SAM3X):
	CHIP_ID = 0x285E0A60
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 256)


@Part.UntestedPart
class ATSAM3X4E(SAM3X):
	CHIP_ID = 0x285B0960
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 128)


@Part.UntestedPart
class ATSAM3X8C(SAM3X):
	CHIP_ID = 0x284E0A60
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 256)


@Part.UntestedPart
class ATSAM3X4C(SAM3X):
	CHIP_ID = 0x28A70CE0
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 128)


@Part.UntestedPart
class ATSAM3A8C(SAM3X):
	CHIP_ID = 0x283E0A60
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 256)


@Part.UntestedPart
class ATSAM3A4C(SAM3X):
	CHIP_ID = 0x283B0960
	def __init__(self, samba):
		SAM3X.__init__(self, samba, 2, 2 * 128)
