#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import abc
import logging


class CantSetFlashBoot(Exception):
	def __init__(self, message):
		Exception.__init__(message)


class PartBase(object):
	"""Base class for supported SAM-BA devices. Derived instances should
	   override all methods listed here.
	"""

	__metaclass__ = abc.ABCMeta

	LOG = logging.getLogger(__name__)

	PART_UNTESTED = False


	def is_tested(self):
		"""Determines if the current part has been tested (if not, a warning
		   message should be displayed).

		   Returns:
			   `True` if the part has been physically verified as working,
			   `False` otherwise.
		"""
		return not self.PART_UNTESTED


	@abc.abstractmethod
	def get_name(self):
		"""Device name, as a short string that can be displayed to the user or
		   matched against a requested device name.

		Returns:
			Name of the device, as a string.
		"""
		pass


	@staticmethod
	@abc.abstractmethod
	def identify(ids):
		"""Determines if a device matches the given ID values that have been
		   extracted from the part via a `ChipIdentifier` module.

		Args:
			ids -- dict of chip identifiers being tested { id_name: id_values, }.

		Returns:
			`True` if the part matches the given identifier.
		"""
		pass


	@abc.abstractmethod
	def get_info(self):
		"""Read special registers. This varying for different flash controllers.

		Returns:
			part info as text.
		"""
		pass


	@abc.abstractmethod
	def set_flash_boot(self):
		"""Sets the device boot from a flash.

		May raise exceptions:
			CantSetFlashBoot
		"""
		pass


	@abc.abstractmethod
	def reset(self):
		"""Resets the device."""
		pass


	@abc.abstractmethod
	def run_application(self, samba):
		"""Runs the application from the start of the device's application area.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""
		pass


	@abc.abstractmethod
	def erase_chip(self, samba):
		"""Erases the device's application area.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""
		pass


	@abc.abstractmethod
	def program_flash(self, samba, data, address=None):
		"""Program's the device's application area.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			data    -- Data to program into the device.
			address -- Address to program from (or start of application area if `None`).
		"""
		pass


	@abc.abstractmethod
	def verify_flash(self, samba, data, address=None):
		"""Verifies the device's application area against a reference data set.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			data    -- Data to verify against.
			address -- Address to verify from (or start of application area if `None`).

		Returns:
			`None` if the given data matches the data in the device at the
			specified offset, or a `(address, actual_word, expected_word)`
			tuple of the first mismatch.
		"""
		pass


	@abc.abstractmethod
	def read_flash(self, samba, address=None, length=None):
		"""Reads the device's application area.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			address -- Address to read from (or start of application area if `None`).
			length  -- Length of the data to extract (or until end of application area if `None`).

		Returns:
			Byte array of the extracted data.
		"""
		pass


def UntestedPart(part):
	"""Decorator applied to parts who have not yet been physically tested to
	   ensure they work as expected.
	"""

	if not issubclass(part, PartBase):
		raise TypeError('Untested part decorator is for Part instances only.')

	part.PART_UNTESTED = True
	return part
