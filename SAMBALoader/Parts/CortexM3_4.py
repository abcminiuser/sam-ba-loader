
from __future__ import print_function
import logging
from . import Part
from .. import FlashControllers


class CortexM3_4(Part.PartBase):
	"""Common part implementation for the Cortex M4 family devices.

	It's expected to inheritors to set the variables:
	self.flash_address_range as AddressRange -- entire flash address region
	self.flash_controllers as list of FlashControllerBase -- flash planes with each own controller
	self.reset_controller as RSTC -- reset controller (optional)
	"""

	LOG = logging.getLogger(__name__)

	def __init__(self, samba):
		self.samba = samba


	@classmethod
	def get_name(cls):
		"""Retrieves the part name as a string. This extracts out the actual
		   class name of the sub-classed parts.

		Returns:
			Name of the SAM part, as a string (empty string for base classes).
		"""
		return '' if cls is CortexM3_4 else cls.__name__


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


	def get_info(self):
		"""Read special registers.

		Returns:
			part info as text.
		"""
		ret = ''
		ret += self.flash_controllers[0].get_info()
		return ret


	def set_flash_boot(self):
		"""Sets the device boot from a flash."""
		# set GPNVM bits
		self.flash_controllers[0].set_gpnvm(2)
		# check GPNVM bits
		buff = self.flash_controllers[0].read_gpnvm()
		if buff & 2 == 0:
			raise Part.CantSetFlashBoot('Can''t set boot from a flash. GPNVM bits: 0x{0:X} ({0})'.format(buff))


	def reset(self):
		"""Resets the device."""
		if hasattr(self, 'reset_controller') and hasattr(self.reset_controller, 'reset'):
			self.reset_controller.reset()
		else:
			self.LOG.warn('No reset for this device')


	def run_application(self, address):
		"""Runs the application from the specified address.
		"""
		self.samba.run_from_address(address)


	def erase_chip(self, address=None):
		"""Erases the flash plane or chip.

		Args:
			address -- Address of flash plane to erase (or chip erase if `None`).
		"""

		for flash_controller in self.flash_controllers:
			if address is None or flash_controller.flash_address_range.is_in_range(address, 0):
				flash_controller.erase_flash(None)


	def program_flash(self, data, address=None):
		"""Program's the device's application area.

		Args:
			data    -- Data to program into the device.
			address -- Address to program from (or start of application area if `None`).
		"""

		pages_address_and_data = self.flash_address_range.get_page_chunks(data, address)
		for page_index, page_address_and_data in enumerate(pages_address_and_data):
			if page_address_and_data:
				if not self.flash_controllers[page_index].program_flash(page_address_and_data[1], page_address_and_data[0]):
					return False
		return True


	def verify_flash(self, data, address=None):
		"""Verifies the device's application area against a reference data set.

		Args:
			data    -- Data to verify against.
			address -- Address to verify from (or start of flash if `None`).
		"""

		if address is None:
			address = self.flash_address_range.start
		pages_address_and_data = self.flash_address_range.get_page_chunks(address, data)
		for page_index, page_address_and_data in enumerate(pages_address_and_data):
			if page_address_and_data:
				if not self.flash_controllers[page_index].verify_flash(page_address_and_data[1], page_address_and_data[0]):
					return False
		return True


	def read_flash(self, address=None, length=None):
		"""Reads the device's application area.

		Args:
			address -- Address to read from (or start of flash if `None`).
			length  -- Length of the data to extract (or until end of flash if `None`).

		Returns:
			Byte array of the extracted data.
		"""

		ret = bytearray()
		pages_address_and_length = self.flash_address_range.get_page_addresses(address, length)
		for page_index, page_address_and_length in enumerate(pages_address_and_length):
			if page_address_and_length:
				ret += self.flash_controllers[page_index].read_flash(page_address_and_length[0], page_address_and_length[1])
		return ret
