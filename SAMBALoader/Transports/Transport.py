#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import abc
import logging



class TimeoutError(Exception):
	"""Exception thrown when a read operation times out while waiting for more
	   data.
	"""
	pass



class TransportBase(object):
	"""Base class for SAM-BA transports. Derived instances should override all
	   methods listed here.
	"""

	__metaclass__ = abc.ABCMeta

	LOG = logging.getLogger(__name__)


	@abc.abstractmethod
	def read(self, length):
		"""Reads a given number of bytes from the transport.

		Args:
			length -- Number of bytes to read. If `None`, a full line will be
						read until a terminator is reached.

		Returns:
			Byte array of the received data.
		"""
		pass


	@abc.abstractmethod
	def write(self, data):
		"""Writes a given number of bytes to the transport.

		Args:
			data -- Bytes to write.
		"""
		pass
