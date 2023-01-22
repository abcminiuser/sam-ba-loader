#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Transport
import logging
import io


class XMODEM(Transport.TransportBase):
	"""XMODEM wrapper transport."""


	def __init__(self, transport):
		"""Constructs an XMODEM transport.

		Args:
			transport -- Existing transport to wrap with an XMODEM stream.
		"""

		try:
			import xmodem
		except ImportError as e:
			self.LOG.fatal('Could not import xmodem library. Is it installed?')
			raise e

		if not isinstance(transport, Transport.TransportBase):
			raise AssertionError('XMODEM transport must wrap an existing transport instance.')

		self.transport = transport
		self.xmodem    = xmodem.XMODEM(self._read_byte, self._write_byte)


	def _read_byte(self, size, timeout=1):
		"""Internal helper for the XMODEM serialiser, to bind read requests to
		   the wrapped transport.

		   Args:
			  size    -- length of the data to read.
			  timeout -- read timeout, in seconds.

		   Returns:
			  Read data as an array of bytes.
		"""

		return self.transport.read(size)


	def _write_byte(self, data, timeout=1):
		"""Internal helper for the XMODEM serialiser, to bind write requests to
		   the wrapped transport.

		   Args:
			  data    -- data to send.
			  timeout -- write timeout, in seconds.

		   Returns:
			  Read data as an array of bytes.
		"""

		self.transport.write(data)
		return len(data)


	def read(self, length):
		"""Reads a given number of bytes from the wrapped transport over XMODEM.

		Args:
			length -- Number of bytes to read.

		Returns:
			Byte array of the received data.
		"""

		data = io.BytesIO()
		self.xmodem.recv(data, crc_mode=1)
		return [ord(b) if isinstance(b, str) else b for b in data.getvalue()]


	def write(self, data):
		"""Writes a given number of bytes to the wrapped transport over XMODEM.

		Args:
			data -- Bytes to write.
		"""

		data = bytearray(data)
		data.extend([255] * (128 - len(data)))

		packet = io.BytesIO(data)
		self.xmodem.send(packet)
