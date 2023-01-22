#
#      Open Source SAM-BA Programmer
#      Released under the MIT license
#
#   dean [at] fourwalledcubicle [dot] com
#         www.fourwalledcubicle.com
#

from . import FileFormats
import logging


def _get_subclasses(classname):
	"""Recursively obtains all subclasses of the given class."""

	subclasses = []

	for p in classname.__subclasses__():
		subclasses.append(p)
		subclasses.extend(_get_subclasses(p))

	return subclasses



class FileFormatLibrary(object):
	"""Part library class, which lists all supported devices and provides
		methods to retrieve a given part by its chip identifiers, or by name.
	"""

	SUPPORTED_FORMATS = _get_subclasses(FileFormats.FileFormatBase)

	LOG = logging.getLogger(__name__)


	@staticmethod
	def find_by_name(filename):
		"""Retrieves a supported file format processor from a filename.

		Args:
			filename -- Filename to check against all file processors.

		Returns:
			List of all format processors which match against the filename.
		"""
		return [f for f in FileFormatLibrary.SUPPORTED_FORMATS if f.can_process(filename)]
