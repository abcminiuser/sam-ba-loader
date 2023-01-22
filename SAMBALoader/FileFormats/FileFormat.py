#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

import abc
import logging


class FileFormatBase(object):
	"""Base class for file format readers. Derived instances should override
	   all methods listed here.
	"""

	__metaclass__ = abc.ABCMeta

	LOG = logging.getLogger(__name__)


	@staticmethod
	@abc.abstractmethod
	def can_process(self, filename):
		"""Determines if the file format can process a given file, based on its
		   filename (usually, this is based on the file extension).

		Args:
			filename -- Filename of the file to examine.

		Returns:
			`True`, if the format reader can parse the given file format.
		"""
		pass


	@abc.abstractmethod
	def get_name(self):
		"""Format reader name, as a short string that can be displayed to the
		   user.

		   Returns:
			   Name of the format reader, as a string.
		"""
		pass


	@abc.abstractmethod
	def read(self, filename):
		"""Reads and parses the contents of a file from disk. The contents of
		   the parsed file are stored internally for later access, as well as
		   returned immediately for convenience.

		Args:
			filename -- Filename of the file to read.

		Returns:
			Iterable of the processed data.
		"""
		pass


	def write(self, filename):
		"""Writes the contents the file to a file on disk.

		Args:
			filename -- Filename of the binary file to write to.
		"""
		pass
