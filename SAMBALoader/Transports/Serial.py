#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import Transport
import logging


class Serial(Transport.TransportBase):
	"""Serial transport for SAM-BA devices using a COM port."""

	LOG = logging.getLogger(__name__)


	def __init__(self, port, baud=115200):
		"""Constructs a Serial transport.

		Args:
			port           -- Serial port to open (e.g. "COM1" or "/dev/ttyACM0").
			baud           -- Baud rate to use.
			log_to_console -- If `True`, traffic will be logged to the console.
		"""

		try:
			import serial
		except ImportError as e:
			self.LOG.fatal('Could not import pyserial library. Is it installed?')
			raise e

		self.LOG.info('Open {} @ {} 8N1'.format(port, baud))
		self.serialport = serial.Serial(port=port,
										baudrate=baud,
										parity=serial.PARITY_NONE,
										stopbits=serial.STOPBITS_ONE,
										bytesize=serial.EIGHTBITS,
										timeout=1, # read timeout, s
										write_timeout=1)

		# flush input buffer
		try:
			self.serialport.flush()
		except:
			pass


	def __del__(self):
		"""Destructor for the Serial transport, closing all resources."""
		try:
			self.serialport.close()
		except:
			pass


	def __str__(self):
		try:
			return self._get_port_properties()
		except:
			pass
		return ''


	def _get_port_properties(self):

		def get_bytesize():
			if self.serialport.bytesize == serial.FIVEBITS:
				return '5'
			elif self.serialport.bytesize == serial.SIXBITS:
				return '6'
			elif self.serialport.bytesize == serial.SEVENBITS:
				return '7'
			return '8'

		def get_parity():
			if self.serialport.parity == serial.PARITY_NONE:
				return 'N'
			elif self.serialport.parity == serial.PARITY_EVEN:
				return 'E'
			elif self.serialport.parity == serial.PARITY_ODD:
				return 'O'
			elif self.serialport.parity == serial.PARITY_MARK:
				return 'M'
			return 'S'

		def get_stopbits():
			if self.serialport.stopbits == serial.STOPBITS_ONE:
				return '1'
			elif self.serialport.stopbits == serial.STOPBITS_ONE_POINT_FIVE:
				return '1.5'
			return '2'

		try:
			import serial
		except:
			pass
		try:
			port_name = self.serialport.port
		except:
			port_name = ''
		try:
			port_baudrate = str(self.serialport.baudrate)
			port_baudrate += ' ' + get_bytesize() + get_parity() + get_stopbits()
		except Exception as e:
			port_baudrate = ''
		else:
			port_baudrate = ' @ ' + port_baudrate
		return port_name + port_baudrate


	def _to_byte_array(self, data):
		"""Encodes an input string or list of values/characters into a flat
		   byte array of bytes. This can be used to convert a Unicode string
		   (using an ASCII only encoding) or list of characters and integers
		   into a flat set of bytes for transmission.

		Args:
			data -- input data to convert

		Returns:
			Flat byte array.
		"""

		if isinstance(data, str):
			return bytearray(data.encode('ascii', 'ignore'))
		else:
			return bytearray([ord(d) if isinstance(d, str) else d for d in data])


	def read(self, length):
		"""Reads a given number of bytes from the serial interface.

		Args:
			length -- Number of bytes to read.

		Returns:
			Byte array of the received data.

		Raises:
			TimeoutError if the read operation timed out.
		"""

		data = self.serialport.read(length)
		if len(data) != length:
			raise Transport.TimeoutError()

		self.LOG.debug('Receive %d bytes %s' % (len(data), [b for b in data]))

		return bytearray(data)


	def write(self, data):
		"""Writes a given number of bytes to the serial interface.

		Args:
			data -- Bytes to write.
		"""

		self.LOG.debug('Send %d bytes: %s' % (len(data), [b for b in data]))

		self.serialport.write(self._to_byte_array(data))
