#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import FlashController


class NVMCTRL(FlashController.FlashControllerBase):
	CTRLA_OFFSET     = 0x0000
	CTRLB_OFFSET     = 0x0004
	PARAM_OFFSET     = 0x0008
	STATUS_OFFSET    = 0x0018
	INTFLAG_OFFSET   = 0x0014
	ADDRESS_OFFSET   = 0x001C

	CTRLB_MANW       = (1 << 7)

	INTFLAG_READY    = (1 << 0)
	INTFLAG_ERROR    = (1 << 1)

	CTRLA_CMDA       = {
		'ER'  : 0x02,
		'WP'  : 0x04,
		'PBC' : 0x44,
	}

	PAGES_PER_ROW    = 4


	def __init__(self, base_address):
		"""Initializes a NVMCTRL controller instance.

		Args:
			base_address -- Absolute base address of the NVMCTRL module
		"""

		self.base_address = base_address


	def _get_nvm_params(self, samba):
		"""Retrieves the NVM parameters and caches then in the class instance.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""

		nvm_param = samba.read_word(self.base_address + self.PARAM_OFFSET)

		self.page_size = 8 << ((nvm_param >> 16) & 0x07)
		self.pages     = nvm_param & 0xFFFF


	def _wait_while_busy(self, samba):
		"""Waits until the NVM controller is ready for a new operation.

		Args:
			samba -- Core `SAMBA` instance bound to the device.
		"""
		while not samba.read_half_word(self.base_address + self.INTFLAG_OFFSET) & self.INTFLAG_READY:
			pass


	def _command(self, samba, command):
		"""Issues a low-level command to the NVMCTRL module.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			command -- Command value to issue (see `CTRLA_CMDA`)
		"""

		self._wait_while_busy(samba)

		reg  = (0xA5 << 8) | command
		samba.write_half_word(self.base_address + self.CTRLA_OFFSET, reg)


	def get_info(self):
		"""Read special registers.

		Returns:
			flash controller info as text.
		"""
		ret = ''
		return ret


	def erase_flash(self, samba, start_address, end_address=None):
		"""Erases the device's application area in the specified region.

		Args:
			samba         -- Core `SAMBA` instance bound to the device.
			start_address -- Start address to erase.
			end_address   -- End address to erase (or end of application area if `None`).
		"""

		self._get_nvm_params(samba)

		if end_address is None:
			end_address = self.pages * self.page_size

		start_address -= start_address % (self.PAGES_PER_ROW * self.page_size)
		end_address   -= end_address   % (self.PAGES_PER_ROW * self.page_size)

		for offset in range(start_address, end_address, self.PAGES_PER_ROW * self.page_size):
			samba.write_word(self.base_address + self.ADDRESS_OFFSET, offset >> 1)

			self._command(samba, self.CTRLA_CMDA['ER'])
			self._wait_while_busy(samba)


	def program_flash(self, samba, address, data):
		"""Program's the device's application area.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			address -- Address to program from.
			data    -- Data to program into the device.
		"""

		self._get_nvm_params(samba)

		samba.write_word(self.base_address + self.CTRLB_OFFSET, self.CTRLB_MANW)

		self._command(samba, self.CTRLA_CMDA['PBC'])
		self._wait_while_busy(samba)

		for (chunk_address, chunk_data) in self._chunk(self.page_size, address, data):
			for offset in range(0, len(chunk_data), 4):
				word = sum([x << (8 * i) for i, x in enumerate(chunk_data[offset : offset + 4])])
				samba.write_word(chunk_address + offset, word)

			self._command(samba, self.CTRLA_CMDA['WP'])
			self._wait_while_busy(samba)
		return True


	def verify_flash(self, samba, address, data):
		"""Verifies the device's application area against a reference data set.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			address -- Address to verify from.
			data    -- Data to verify against.

		Returns:
			`None` if the given data matches the data in the device at the
			specified offset, or a `(address, actual_word, expected_word)`
			tuple of the first mismatch.
		"""

		for (chunk_address, chunk_data) in self._chunk(self.page_size, address, data):
			actual_data = samba.read_block(chunk_address, len(chunk_data))

			for offset in range(0, len(chunk_data), 4):
				expected_word = sum([x << (8 * i) for i, x in enumerate(chunk_data[offset : offset + 4])])
				actual_word   = sum([x << (8 * i) for i, x in enumerate(actual_data[offset : offset + 4])])

				if actual_word != expected_word:
					return (chunk_address + offset, actual_word, expected_word)

		return None


	def read_flash(self, samba, address, length=None):
		"""Reads the device's application area.

		Args:
			samba   -- Core `SAMBA` instance bound to the device.
			address -- Address to read from.
			length  -- Length of the data to extract (or until end of application area if `None`).

		Returns:
			Byte array of the extracted data.
		"""

		self._get_nvm_params(samba)

		if length is None:
			length = (self.pages * self.page_size) - address

		return samba.read_block(address, length)
