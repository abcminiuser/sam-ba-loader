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


class SAM4S(CortexM3_4):
	"""Base part class for SAM4S series."""


	def __init__(self, samba, flash_planes, flash_total_length):
		"""Initializes class with flash & RSTC

		Args:
			flash_planes       -- flash planes & controllers count: 1 or 2
			flash_total_length -- total flash length, kBytes
		"""
		CortexM3_4.__init__(self, samba)
		self.flash_address_range = AddressRange(0x00400000, flash_total_length * 1024, int((flash_total_length * 1024) // flash_planes))
		if flash_planes == 1:
			self.flash_controllers = (
				EEFCFlash.Flash(self.samba, 0x00400000, 0x400E0A00, flash_total_length * 2, 512),
				)
		else:
			self.flash_controllers = (
				EEFCFlash.Flash(self.samba, 0x00400000, 0x400E0A00, flash_total_length, 512),
				EEFCFlash.Flash(self.samba, 0x00400000 + flash_total_length * 512, 0x400E0C00, flash_total_length, 512),
				)
		self.reset_controller = RSTC(samba, 0x400E1400)


	@classmethod
	def identify(cls, ids):
		if not hasattr(cls, 'CHIP_ID'):
			return False
		try:
			chip_id = ids['CHIPID'].chip_id & 0x7FFFFFE0 # remove revision (A, B)
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
		return '' if cls is SAM4S else cls.__name__


@Part.UntestedPart
class ATSAM4SD32C(SAM4S):
	CHIP_ID = 0x29A70EE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 2, 2 * 1024)


@Part.UntestedPart
class ATSAM4SD32B(SAM4S):
	CHIP_ID = 0x29970EE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 2, 2 * 1024)


class ATSAM4SD16C(SAM4S):
	CHIP_ID = 0x29A70CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 2, 1024)


@Part.UntestedPart
class ATSAM4SD16B(SAM4S):
	CHIP_ID = 0x29970CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 2, 1024)


@Part.UntestedPart
class ATSAM4SA16C(SAM4S):
	CHIP_ID = 0x28A70CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 1024)


@Part.UntestedPart
class ATSAM4SA16B(SAM4S):
	CHIP_ID = 0x28970CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 1024)


@Part.UntestedPart
class ATSAM4S16B(SAM4S):
	CHIP_ID = 0x289C0CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 1024)


@Part.UntestedPart
class ATSAM4S16C(SAM4S):
	CHIP_ID = 0x28AC0CE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 1024)


@Part.UntestedPart
class ATSAM4S8B(SAM4S):
	CHIP_ID = 0x289C0AE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 512)


@Part.UntestedPart
class ATSAM4S8C(SAM4S):
	CHIP_ID = 0x28AC0AE0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 512)


@Part.UntestedPart
class ATSAM4S4C(SAM4S):
	CHIP_ID = 0x28AB09E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 256)


@Part.UntestedPart
class ATSAM4S4B(SAM4S):
	CHIP_ID = 0x289B09E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 256)


@Part.UntestedPart
class ATSAM4S4A(SAM4S):
	CHIP_ID = 0x288B09E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 256)


@Part.UntestedPart
class ATSAM4S2C(SAM4S):
	CHIP_ID = 0x28AB07E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 128)


@Part.UntestedPart
class ATSAM4S2B(SAM4S):
	CHIP_ID = 0x289B07E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 128)


@Part.UntestedPart
class ATSAM4S2A(SAM4S):
	CHIP_ID = 0x288B07E0
	def __init__(self, samba):
		SAM4S.__init__(self, samba, 1, 128)
