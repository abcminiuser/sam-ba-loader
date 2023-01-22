#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Part
from .. import FlashControllers


class CortexM0p(Part.PartBase):
	"""Common part implementation for the Cortex M0+ family devices."""

	# FLASH_CONTROLLER   = FlashControllers.NVMCTRL(base_address=0x41004000)

	BOOTLOADER_SIZE    = 2048
	FLASH_BASE_ADDRESS = 0x00000000
	FLASH_APP_ADDRESS  = FLASH_BASE_ADDRESS + BOOTLOADER_SIZE


	@classmethod
	def get_name(cls):
		"""Retrieves the part name as a string. This extracts out the actual
		   class name of the sub-classed parts, on the assumption that all
		   subclasses of this class will be a specific SAM part (e.g.
		   SAMD20J18A).

		   Returns:
			   Name of the SAM part, as a string.
		"""
		return '' if cls is CortexM0p else cls.__name__


	@staticmethod
	def identify(ids):
		"""Determines if a device matches the given ID values that have been
		   extracted from the part via a `ChipIdentifier` module. This is a
		   common family implementation intended to be sub-classes per-device,
		   thus this always returns a failed match.

		Args:
			ids -- dict of chip identifiers being tested { id_name: id_values, }.

		Returns:
			`False`.
		"""
		return False


	def __init__(self, samba):
		self.samba = samba


	def get_info(self):
		"""Read special registers.

		Returns:
			part info as text.
		"""
		ret = ''
		return ret


	def set_flash_boot(self):
		"""Sets the device boot from a flash."""
		pass


	def reset(self):
		"""Resets the device."""
		pass


	def run_application(self):
		"""Runs the application from the start of the device's application area.
		"""
		self.samba.run_from_address(self.FLASH_APP_ADDRESS)


	def erase_chip(self, address=None):
		"""Erases the device's application area. As these SAM devices do not
		   contain a ROM based SAM-BA bootloader, this is massaged into a range
		   erase of the flash from the end of the bootloader area to the end of
		   the flash.
		"""
		self.FLASH_CONTROLLER.erase_flash(self.samba, start_address=self.FLASH_APP_ADDRESS)


	def program_flash(self, data, address=None):
		"""Program's the device's application area.

		Args:
			data    -- Data to program into the device.
			address -- Address to program from (or start of application area if `None`).
		"""

		if address is None:
			address = self.FLASH_APP_ADDRESS

		self.FLASH_CONTROLLER.program_flash(self.samba, address, data)


	def verify_flash(self, data, address=None):
		"""Verifies the device's application area against a reference data set.

		Args:
			data    -- Data to verify against.
			address -- Address to verify from (or start of application area if `None`).

		Returns:
			`None` if the given data matches the data in the device at the
			specified offset, or a `(address, actual_word, expected_word)`
			tuple of the first mismatch.
		"""

		if address is None:
			address = self.FLASH_APP_ADDRESS

		return self.FLASH_CONTROLLER.verify_flash(self.samba, address, data)


	def read_flash(self, address=None, length=None):
		"""Reads the device's application area.

		Args:
			address -- Address to read from (or start of application area if `None`).
			length  -- Length of the data to extract (or until end of application area if `None`).

		Returns:
			Byte array of the extracted data.
		"""

		if address is None:
			address = self.FLASH_APP_ADDRESS

		return self.FLASH_CONTROLLER.read_flash(self.samba, address, length=length)
