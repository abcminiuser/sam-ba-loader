#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

# Enhanced Embedded Flash Controller (EEFC) driver for Atmel SAM

from time import time, sleep
import logging

from . import FlashController


class CommandException(Exception):
	def __init__(self, fsr_address, fsr):
		self.fsr_address = fsr_address
		self.fsr = fsr
	def __str__(self):
		return 'Command error EEFC_FSR @ {:08X}: {:08X}'.format(self.fsr_address, self.fsr)


class Flash(FlashController.FlashControllerBase):
	FMR_OFFSET = 0x00 # Flash Mode Register
	FCR_OFFSET = 0x04 # Flash Command Register
	FSR_OFFSET = 0x08 # Flash Status Register
	FRR_OFFSET = 0x0c # Flash Result Register

	FCR_FKEY = 0x5a000000

	FSR_MASK = {
		'FRDY' : 1, # Flash Ready Status (cleared when Flash is busy)
		'FCMDE' : 2, # Flash Command Error Status (cleared on read or by writing EEFC_FCR)
		'FLOCKE' : 4, # Flash Lock Error Status (cleared on read)
		'FLERR' : 8, # Flash Error Status (cleared when a programming operation starts)
	}

	FCR_CMDA = {
		'GETD' : 0x00, # Get Flash descriptor
		'WP' : 0x01, # Write page
		'WPL' : 0x02, # Write page and lock
		'EWP' : 0x03, # Erase page and write page
		'EWPL' : 0x04, # Erase page and write page then lock
		'EA' : 0x05, # Erase all
		'EPA' : 0x07, # Erase pages
		'SLB' : 0x08, # Set lock bit
		'CLB' : 0x09, # Clear lock bit
		'GLB' : 0x0A, # Get lock bit
		'SGPB' : 0x0B, # Set GPNVM bit
		'CGPB' : 0x0C, # Clear GPNVM bit
		'GGPB' : 0x0D, # Get GPNVM bit
		'STUI' : 0x0E, # Start read unique identifier
		'SPUI' : 0x0F, # Stop read unique identifier
		'GCALB' : 0x10, # Get CALIB bit
		'ES' : 0x11, # Erase sector
		'WUS' : 0x12, # Write user signature
		'EUS' : 0x13, # Erase user signature
		'STUS' : 0x15, # Start read user signature
		'SPUS' : 0x14, # Stop read user signature
	}

	LOG = logging.getLogger(__name__)


	def __init__(self, samba, flash_base_address, regs_base_address, pages, page_size, dont_use_read_block=False):
		"""Initializes a Enhanced Embedded Flash Controller (EEFC) instance.

		Args:
			samba              -- Core `SAMBA` instance bound to the device
			flash_base_address -- Absolute base address of the flash region
			regs_base_address  -- Absolute base address of the flash control registers
			pages              -- Pages count
			page_size          -- Page size, bytes
			dont_use_read_block-- SAM3 bugfix: all 0 reads when SAMBA read_block
		"""

		self.samba = samba
		self.flash_address_range = FlashController.AddressRange(flash_base_address, pages * page_size, page_size)
		self.regs_base_address = regs_base_address
		# SAM3 bugfux
		samba.write_word(self.regs_base_address + self.FMR_OFFSET, 0x6 << 8)
		self.dont_use_read_block = dont_use_read_block


	def _wait_while_busy(self, timeout=2):
		"""Waits until the flash controller in the attached device is ready for a new operation.

		Args:
			timeout -- Wait timeout (double), s
		"""
		printed = False
		start_timestamp = time()
		while self.samba.read_word(self.regs_base_address + self.FSR_OFFSET) & self.FSR_MASK['FRDY'] == 0:
			if not printed:
				self.LOG.debug('Flash busy')
				printed = True
			if time() - start_timestamp >= timeout:
				raise Exception('Flash busy: timeout. FSR: ' + str(self.samba.read_word(self.regs_base_address + self.FSR_OFFSET)))
			sleep(.001)

		if printed:
			self.LOG.debug('Flash was busy for {:.3f}s'.format(time() - start_timestamp))


	def _command(self, command='GETD', farg=0, do_not_wait=False):
		"""Issues a low-level command to the NVMCTRL module within the
			connected device.

		Args:
			command     -- Command value to issue (see `FCR_CMDA`)
			farg        -- Command argument value to issue (see `FCR_CMDA`)
			do_not_wait -- do not check busy flag before command issue
		"""

		if not do_not_wait:
			self._wait_while_busy()

		if type(command) is str:
			command = self.FCR_CMDA[command]

		reg  = self.FCR_FKEY | ((farg & 0xFFFF) << 8) | (command & 0xFF)

		self.LOG.debug('EEFC_FCR @ 0x{:08X} = 0x{:08X}'.format(self.regs_base_address + self.FCR_OFFSET, reg))
		self.samba.write_word(self.regs_base_address + self.FCR_OFFSET, reg)
		# check for error
		reg = self.samba.read_word(self.regs_base_address + self.FSR_OFFSET) & ~self.FSR_MASK['FRDY'] & 0xF
		if reg:
			raise CommandException(self.regs_base_address + self.FSR_OFFSET, reg)


	def _read_block(self, address, length):
		"SAM3 bugfux: all 0 reads when SAMBA read_block"
		if self.dont_use_read_block:
			return self._read_by_word(address, length)
		else:
			return self.samba.read_block(address, length)


	def _read_by_word(self, address, length):
		def append_bytes(offset_byte, length=None):
			if length is None:
				length = 4 - offset_byte % 4
			for i in range(offset_byte, offset_byte + length):
				ret.append(buff >> i * 8 & 0xFF)
		ret = bytearray()
		if address % 4 != 0:
			buff = self.samba.read_word(address - address % 4)
			append_bytes(address % 4, min(4 - address % 4, length))
			length -= 4 - address % 4
			address += 4 - address % 4
		for i in range(address, address + length, 4):
			buff = self.samba.read_word(i)
			append_bytes(0, min(address + length - i, 4))
		return ret


	def read_gpnvm(self):
		"Reads GPNVM bits"
		self._command('GGPB')
		self._wait_while_busy()
		buff = self.samba.read_word(self.regs_base_address + self.FRR_OFFSET)
		self.LOG.info('EEFC_FRR @ 0x{:08X}: 0x{:08X}'.format(self.regs_base_address + self.FRR_OFFSET, buff))
		return buff


	def set_gpnvm(self, bits_mask):
		"Sets GPNVM bits according to mask"
		for i, bit in enumerate(bin(bits_mask)[2:][::-1]):
			if bit == '1':
				self._command('SGPB', i)


	def clear_gpnvm(self, bits_mask):
		"Clears GPNVM bits according to mask"
		for i, bit in enumerate(bin(bits_mask)[2:][::-1]):
			if bit == '1':
				self._command('CGPB', i)


	def read_descriptor(self):
		"Reads flash descriptor as list of words"
		self._command()
		self._wait_while_busy()
		start_timestamp = time()
		ret = []
		while True:
			if time() - start_timestamp >= .5:
				raise Exception('Get Flash Descriptor: timeout')
			buff = self.samba.read_word(self.regs_base_address + self.FRR_OFFSET)
			if not buff:
				return ret
			ret.append(buff)
		return ret


	def read_unique_identifier_area(self):
		"Reads unique identifier area as bytearray"
		self._command('STUI')
		# self._wait_while_busy() # The FRDY flag is not set when the STUI command is achieved
		ret = self._read_block(self.flash_address_range.start, 16)
		self._command('SPUI', do_not_wait=True)
		return ret


	def get_info(self):
		"""Read special registers & flash regions.

		Returns:
			flash controller info as text.
		"""
		ret = 'Flash info\n'
		ret += '\tGPNVM bits: ' + str(self.read_gpnvm()) + '\n'
		ret += '\tUnique identifier area: ' + self.read_unique_identifier_area().decode('ascii', 'replace') + '\n'
		ret += '\tDescriptor: ' + str(self.read_descriptor()) + '\n'
		return ret


	def read_flash(self, address=None, length=None):
		"""Reads the data from flash.

		Args:
			address -- Absolute address to read from. If `None` read from start of flash.
			length -- Length of the data to read (or until end of application area if `None`).

		Returns:
			Byte array of the extracted data.
		"""

		if address is None:
			address = self.flash_address_range.start
		if not self.flash_address_range.is_in_range(address, 0):
			raise OutOfRangeException(self.flash_address_range, address)

		if length is None:
			length = self.flash_address_range.remaining_length(address)
		if not self.flash_address_range.is_in_range(address, length):
			raise OutOfRangeException(self.flash_address_range, address)

		self.LOG.debug('Flash read: '+str(FlashController.AddressRange(address, length)))
		ret = self._read_block(address, length)

		return ret


	def program_flash(self, data, address=None):
		"""Writes the data to flash.

		Args:
			data -- Data to write.
			address -- Absolute address to write to. If `None` write from start of flash.
		"""

		if address is None:
			address = self.flash_address_range.start

		if not self.flash_address_range.is_in_range(address, len(data)):
			raise OutOfRangeException(self.flash_address_range, address)

		self.LOG.info('Flash write: '+str(FlashController.AddressRange(address, len(data))))

		# write to chip flash page by page
		# 32-bit words must be written continuously, in either ascending or descending order.
		# Writing the latch buffer in a random order is not permitted.
		self._wait_while_busy()
		start_timestamp = time()
		for (chunk_address, chunk_data) in self._chunk(self.flash_address_range.page_size, address, data):
			# write to page
			self.LOG.debug('Flash read & compare: '+str(FlashController.AddressRange(chunk_address, len(chunk_data))))
			buff = self._read_block(chunk_address, len(chunk_data))
			if self._is_equal(chunk_data, buff):
				self.LOG.info('Flash compare: equals, not need to write: '+str(FlashController.AddressRange(chunk_address, len(chunk_data))))
			else:
				# checks it's needs to turn from 0 to 1 for any bit
				need_erase = False
				for i in range(len(buff)):
					if buff[i] & chunk_data[i] != chunk_data[i]:
						need_erase = True
						break
				# align: 32 bit words or page size
				align_bytes = self.flash_address_range.page_size if need_erase else 4
				# check chunk data for aligned boundary
				if chunk_address % align_bytes != 0:
					# start of chunk data not aligned # add bytes to chunk data
					new_address = chunk_address - chunk_address % align_bytes
					buff = self._read_block(new_address, chunk_address % align_bytes)
					chunk_data = list(buff) + chunk_data
					chunk_address = new_address
				# now chunk_address is aligned
				if len(chunk_data) % align_bytes != 0:
					# end of chunk data not aligned
					buff = self._read_block(chunk_address + len(chunk_data), align_bytes - len(chunk_data) % align_bytes)
					chunk_data += list(buff)
				# now chunk_address & chunk_data is aligned
				# write to page buffer with 32 bit words
				for i in range(0, len(chunk_data), 4):
					buff = chunk_data[i] | chunk_data[i + 1] << 8 | chunk_data[i + 2] << 16 | chunk_data[i + 3] << 24
					self.samba.write_word(chunk_address + i, buff)
				self._command('EWP' if need_erase else 'WP', chunk_address // self.flash_address_range.page_size)
				self._wait_while_busy()
				# check the chunk
				if not self.verify_flash(chunk_data, chunk_address):
					raise Exception('Flash write error: page address [0x{:08X}..0x{:08X}]'.format(chunk_address, chunk_address + self.flash_address_range.page_size))

		self.LOG.info('Flash was wrote for {:.3f}s'.format(time() - start_timestamp))

		# check the entire data
		return self.verify_flash(data, address)


	def erase_flash(self, start_address=None):
		"""Erases the flash: entire plane, sector, page. Now support entire plane only (`start_address=None`)"""
		if start_address is not None:
			raise Exception('Erase sector or page not supported yet')
		self._command('EA')


	def verify_flash(self, data, address=None):
		"""Verifies the flash data with a reference data"""
		if address is None:
			address = self.flash_address_range.start
		self.LOG.debug('Flash verify: '+str(FlashController.AddressRange(address, len(data))))
		buff = self.read_flash(address, len(data))
		ret = self._is_equal(buff, data)
		if ret:
			self.LOG.info('Flash verify '+str(FlashController.AddressRange(address, len(data)))+': OK')
		else:
			self.LOG.error('Flash verify '+str(FlashController.AddressRange(address, len(data)))+': FAIL')
		return ret
