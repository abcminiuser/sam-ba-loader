#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import logging


class RSTC(object):
	"""Reset Controller (RSTC)."""

	CR_OFFSET = 0x00 # Reset Controller Control Register
	SR_OFFSET = 0x04 # Reset Controller Status Register
	MR_OFFSET = 0x08 # Reset Controller Mode Register

	RSTC_KEY = 0xa5000000


	LOG = logging.getLogger(__name__)

	def __init__(self, samba, base_address):
		"""Initializes a Reset Controller (RSTC) instance.

		Args:
			samba        -- Core `SAMBA` instance bound to the device
			base_address -- Absolute base address of the reset controller registers
		"""

		self.samba = samba
		self.base_address = base_address


	def reset(self, reg=0xD):
		"""Issue the system reset thru RSTC_CR register.

		reg -- Bits: 0 - no effect; 1 - reset
		"""
		reg |= self.RSTC_KEY
		self.LOG.info('RSTC_CR @ 0x{:08X} = 0x{:08X}'.format(self.base_address + self.CR_OFFSET, reg))
		self.samba.write_word(self.base_address + self.CR_OFFSET, reg)


	def status(self):
		"""Reads the status register."""
		ret = self.samba.read_word(self.base_address + self.SR_OFFSET)
		self.LOG.info('RSTC_SR @ 0x{:08X}: 0x{:08X}'.format(self.base_address + self.SR_OFFSET, ret))
		return ret


	def set_mode(self, reg):
		"""Writes the mode register."""
		reg |= self.RSTC_KEY
		self.LOG.info('RSTC_MR @ 0x{:08X} = 0x{:08X}'.format(self.base_address + self.MR_OFFSET, reg))
		self.samba.write_word(self.base_address + self.MR_OFFSET)


	def mode(self):
		"""Reads the mode register."""
		ret = self.samba.read_word(self.base_address + self.MR_OFFSET)
		self.LOG.info('RSTC_MR @ 0x{:08X}: 0x{:08X}'.format(self.base_address + self.MR_OFFSET, ret))
		return ret
