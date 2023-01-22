#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import logging
from . import Parts
from . import ChipIdentifiers
from . import FlashControllers


def _get_subclasses(classname):
	"""Recursively obtains all subclasses of the given class."""

	subclasses = []

	for p in classname.__subclasses__():
		subclasses.append(p)
		subclasses.extend(_get_subclasses(p))

	return subclasses


class CannotRecognizeChipException(Exception):
	def __init__(self, message='', register_name=None, register_addresses=None):
		"""
		Args:
			message            -- text message
			register_name      -- identifier register name
			register_addresses -- list of register addresses [ REGISTER_ADDRESS, ]
		"""
		Exception.__init__(self, message)
		self.register_name = register_name
		self.register_addresses = register_addresses



	def __str__(self):
		addresses = '; register addresses: ' + \
			', '.join([ hex(i) for i in self.register_addresses ]) if self.register_addresses else ''
		register_name = '; register name: ' + self.register_name if self.register_name else ''
		return (self.message if self.message else 'Can\'t recognize chip') + register_name + addresses


class PartLibrary(object):
	"""Part library class, which lists all supported devices and provides
	   methods to retrieve a given part by its chip identifiers, or by name.
	"""

	SUPPORTED_PARTS = _get_subclasses(Parts.PartBase)

	LOG = logging.getLogger(__name__)

	# The chip identifier register dictionary
	# with multiple addresses for different device families
	DEFAULT_ADDRESSES = {
		'CPUID' : [ 0xE000ED00, ],
		'CHIPID' : [ 0x400E0740, 0x400E0940 ], # SAM4, SAM3
		'DSU' : [ 0x41002000, ], # Cortex-M0 devices
		}


	@staticmethod
	def get_chip_ids(samba, addresses=None):
		"""Reads out the chip identifiers from the attached device. Note that
		   each device usually implements only a single one of the chip
		   identifier modules, thus all but one value will essentially read as
		   garbage.

		Args:
			samba     -- Core `SAMBA` instance bound to the device.
			addresses -- Dict: { REGISTER_NAME : REGISTER_ADDRESS, }. If `None`: DEFAULT_ADDRESSES

		Returns:
			Dictionary of `{name, identifiers}` for each chip identifier,
			which can then be used to match against a device.
		"""

		def create_identifier_register(register_class, register_name):
			# get list of register addresses
			register_addresses = [ addresses[register_name], ] if addresses and register_name in addresses \
				else PartLibrary.DEFAULT_ADDRESSES[register_name]
			# try to create register class 
			for register_address in register_addresses:
				reg = register_class(base_address=register_address)
				if reg.read(samba):
					identifiers[register_name] = reg
					return
			raise CannotRecognizeChipException(register_name=register_name, register_addresses=register_addresses)


		identifiers = dict()

		create_identifier_register(ChipIdentifiers.CPUID, 'CPUID')

		if identifiers['CPUID'].part in identifiers['CPUID'].PART:
			# Cortex-M0 devices have a DSU for additional information, others use a CHIPID
			if 'M0' in identifiers['CPUID'].PART[identifiers['CPUID'].part]:
				create_identifier_register(ChipIdentifiers.DSU, 'DSU')
			else:
				create_identifier_register(ChipIdentifiers.CHIPID, 'CHIPID')

		return identifiers


	@staticmethod
	def find_by_name(name):
		"""Retrieves a supported device by its name.

		Args:
			name -- Name of the device to retrieve

		Returns:
			List of all parts whose name contains the search string.
		"""
		return [p for p in PartLibrary.SUPPORTED_PARTS if p.get_name() == name]


	@staticmethod
	def find_by_chip_ids(chip_ids):
		"""Retrieves a supported device by its chip identifiers.

		Args:
			chip_ids -- Dictionary of `{name, identifiers}` for each chip
						identifier that should be matched against all supported
						devices.

		Returns:
			List of all parts which match against the chip identifiers.
		"""
		return [p for p in PartLibrary.SUPPORTED_PARTS if p.identify(chip_ids)]
