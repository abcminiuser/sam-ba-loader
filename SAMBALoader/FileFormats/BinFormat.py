#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import FileFormat


class BinFormat(FileFormat.FileFormatBase):
	def __init__(self):
		"""Constructor for the bin file format processor."""

		self.data = []


	def __setitem__(self, index, value):
		self.data[index] = value


	def __getitem__(self, index):
		return self.data[index]


	def __len__(self):
		return len(self.data)


	@staticmethod
	def can_process(filename):
		filename_components = filename.split('.')
		if len(filename_components) < 2:
			return False

		return filename.split('.')[-1] == "bin"


	def get_name(self):
		return "Binary"


	def read(self, filename):
		"""Reads and parses the contents of a binary file from disk.

		Args:
			filename -- Filename of the binary file to read.

		Returns:
			Iterable of the processed data.
		"""

		with open(filename, 'rb') as f:
			self.data = [ord(b) if isinstance(b, str) else b for b in f.read()]

		self.LOG.debug('Read bin file \'%s\' (%d bytes)' % (filename, len(self.data)))
		return self


	def write(self, filename):
		"""Writes the contents the file to a binary file on disk.

		Args:
			filename -- Filename of the binary file to write to.
		"""

		with open(filename, 'wb') as f:
			f.write(self.data)

		self.LOG.debug('Wrote bin file \'%s\' (%d bytes)' % (filename, len(self.data)))
