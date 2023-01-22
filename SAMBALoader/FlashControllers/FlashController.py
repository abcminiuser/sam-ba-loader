#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import abc
import logging


class OutOfRangeException(Exception):
	def __init__(self, flash_address_range, address, length=None):
		self.address, self.length = address, length
		self.flash_address_range = flash_address_range


	def __str__(self):
		if self.length:
			return 'Out of range of flash space: available {}; given {}'.format(
				str(self.flash_address_range), str(FlashController.AddressRange(self.address, self.length, 0)))
		else:
			return 'Out of range of flash space: available {0}; given 0x{1:08X} ({1})'.format(
				str(self.flash_address_range), self.address)


class AddressRange():
	def __init__(self, start, length, page_size=None):
		self.start, self.length = start, length
		self.page_size = page_size


	def __str__(self):
		return '[0x{0:08X}..0x{2:08X}] 0x{1:X} ({1})'.format(self.start, self.length, self.start + self.length)


	@property
	def pages_count(self):
		try:
			return self.length // self.page_size
		except:
			raise Exception('Flash hasn''t pages')


	def is_in_range(self, start, length):
		"Returns True if start and length entire in range"
		return start >= self.start \
			and length >= 0 and length <= self.length \
			and (start - self.start) + length <= self.length


	def remaining_length(self, start):
		if not self.is_in_range(start, 0):
			raise OutOfRangeException(Flash.AddressRange(self.start, self.length), start)
		return self.length - (start - self.start)


	def get_page_chunks(self, data, start=None):
		"""Splits data to chunks for all pages.

		Args:
			address -- Absolute address of data. If `None` then `self.start` address.
			data -- Data to split to pages.

		Returns list of (page_address, page_data)
		"""
		if start is None:
			start = self.start
		if not self.is_in_range(start, len(data)):
			raise OutOfRangeException(self, start, len(data))
		end = start + len(data)
		ret = []
		for page_address in range(self.start, self.start + self.length, self.page_size):
			if page_address < end and page_address + self.page_size > start:
				# move data chunk to ret
				page_data_len = min(len(data), self.page_size - (start - page_address))
				ret.append((start, data[:page_data_len]))
				start += page_data_len
				data = data[page_data_len:]
			else:
				ret.append(None)
		return ret


	def get_page_addresses(self, start=None, length=None):
		"""Gets start address & length for each page.

		Args:
			start -- Absolute address of region. If `None` then `self.start` address.
			length -- Length of region. If `None` then `self.length`.

		Returns list of (address, length)
		"""
		if start is None:
			start = self.start
		elif not self.is_in_range(start, 0):
			raise OutOfRangeException(self, start, length)
		if length is None:
			length = self.remaining_length(start)
		elif not self.is_in_range(start, length):
			raise OutOfRangeException(self, start, length)
		end = start + length
		ret = []
		for page_address in range(self.start, self.start + self.length, self.page_size):
			if page_address < end and page_address + self.page_size > start:
				page_length = min(length, self.page_size - (start - page_address))
				ret.append((start, page_length))
				start += page_length
				length -= page_length
			else:
				ret.append(None)
		return ret


class FlashControllerBase(object):
	"""Base class for SAM Flash controllers.
	"""

	__metaclass__ = abc.ABCMeta

	LOG = logging.getLogger(__name__)


	@staticmethod
	def _chunk(flash_page_size, address, data):
		"""Helper method for subclasses; chunks the given data into flash pages,
		   aligned to single flash pages within the target's address space.

		Args:
			flash_page_size -- Size of each flash page in the target device.
			address         -- Start address of the data to write to.
			data            -- Data to be written to the target device.

		Returns:
			Generator of (address, chunk) tuples for each chunk of data to
			write.
		"""

		chunk = []

		for offset in range(len(data)):
			if offset and (address + offset) % flash_page_size == 0:
				yield (address, chunk)

				address += flash_page_size
				chunk = []

			chunk.append(data[offset])

		if len(chunk):
			yield (address, chunk)


	@staticmethod
	def _is_equal(buff1, buff2):
		for i in range(len(buff1)):
			if buff1[i] != buff2[i]:
				return False
		return True


	@abc.abstractmethod
	def get_info(self):
		"""Read special registers. This varying for different flash controllers.

		Returns:
			flash controller info as text.
		"""
		pass


	@abc.abstractmethod
	def erase_flash(self, start_address=None):
		"""Erases the device's application area in the specified region.

		Args:
			start_address -- Start address to erase (if `None` then start address of flash).
		"""
		pass


	@abc.abstractmethod
	def program_flash(self, data, address=None):
		"""Program's the device's application area.

		Args:
			data    -- Data to program into the device.
			address -- Address to programm from (if `None` then start address of flash).
		"""
		pass


	@abc.abstractmethod
	def verify_flash(self, data, address=None):
		"""Verifies the device's application area against a reference data set.

		Args:
			address -- Address to verify from (if `None` then start address of flash).
			data    -- Data to verify against.

		Returns:
			`None` if the given data matches the data in the device at the
			specified offset, or a `(address, actual, expected)` tuple of the
			first mismatch.
		"""
		pass


	@abc.abstractmethod
	def read_flash(self, address=None, length=None):
		"""Reads the device's application area.

		Args:
			address -- Address to read from (if `None` then start address of flash).
			length  -- Length of the data to extract (or until end of
					application area if `None`).

		Returns:
			Byte array of the extracted data.
		"""
		pass
