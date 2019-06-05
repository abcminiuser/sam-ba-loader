#!/usr/bin/env python

#      Open Source SAM-BA Programmer
#     Copyright (C) Dean Camera, 2016.
#     Copyright (C) Victoria Danchenko, 2019.
#
#  dean [at] fourwalledcubicle [dot] com
#       www.fourwalledcubicle.com
#
#
# Released under a MIT license, see LICENCE.txt.

from __future__ import print_function
import sys
from datetime import datetime
import logging
import argparse
try:
	xrange
except NameError:
	# Remap xrange to range for Python 3
	xrange = range
import SAMBALoader
import SAMBALoader.Transports
from SAMBALoader.FileFormats import BinFormat


class SessionError(Exception):
	pass


class Session(object):

	def __init__(self, samba):
		self.samba = samba
		self.part  = None


	def _get_part(self, chip_ids):
		# find & collect the part classes types by chip ids
		matched_parts = SAMBALoader.PartLibrary.find_by_chip_ids(chip_ids)

		if len(matched_parts) == 0:
			raise SessionError('Unknown part.')
		elif len(matched_parts) > 1:
			raise SessionError('Multiple matching parts: %s' % [p.get_name() for p in matched_parts])
		else:
			# create part class instance
			return matched_parts[0](self.samba)


	def _get_file_processor(self, filename):
		matched_formats = SAMBALoader.FileFormatLibrary.find_by_name(filename)

		if len(matched_formats) == 0:
			raise SessionError('Unknown file format: %s' % filename)
		elif len(matched_formats) > 1:
			raise SessionError('Multiple matching file formats: %s' % [f.get_name() for f in matched_formats])
		else:
			return matched_formats[0]()


	def get_part_identifiers(self, addresses=None):
		"""Reads out the chip identifiers from the attached device. Note that
		   each device usually implements only a single one of the chip
		   identifier modules, thus all but one value will essentially read as
		   garbage.

		Args:
			addresses -- Dict: { REGISTER_NAME : REGISTER_ADDRESS, }. If `None`: DEFAULT_ADDRESSES

		Returns:
			Dictionary of `{name, identifiers}` for each chip identifier,
			which can then be used to match against a device.
		"""
		return SAMBALoader.PartLibrary.get_chip_ids(self.samba, addresses)


	def set_part_by_chip_ids(self, chip_ids):
		self.part = self._get_part(chip_ids)

		return self.part


	def program_flash(self, filename):
		if self.part is None:
			raise SessionError('Part not set.')

		file_format = self._get_file_processor(filename)
		file_data   = file_format.read(filename)

		self.part.program_flash(self.samba, data=file_data)


	def verify_flash(self, filename):
		if self.part is None:
			raise SessionError('Part not set.')

		file_format = self._get_file_processor(filename)
		file_data   = file_format.read(filename)

		verify_failure = self.part.verify_flash(self.samba, data=file_data)
		if verify_failure is not None:
			raise SessionError('Verification failure @ 0x%08x: 0x%08x != 0x%08x' % verify_failure)


def dump_buff(buff):
	for i in xrange(0, len(buff), 16):
		buff2 = ''
		for ii in xrange(16):
			buff2 += '{:02X} '.format(buff[i+ii])
		print('{:08X} {}'.format(i, buff2))


def save_to_file(file_path, buff):
	logging.info('Save 0x{0:X} ({0}) byte(s) to binary file "{1}"'.format(len(buff), file_path))
	f = BinFormat()
	f.data = buff
	f.write(file_path)


def read_from_file(file_path):
	if file_path.lower().endswith('.hex'):
		try:
			from intelhex import IntelHex
		except ImportError:
			print('To open HEX files install IntelHex library:\npip install IntelHex\npip3 install IntelHex')
			sys.exit(3)
		ih = IntelHex()
		ih.loadhex(file_path)
		logging.info('Was readed 0x{0:X} ({0}) byte(s): 0x{1:X}..{2:X}'.format(ih.maxaddr() - ih.minaddr() + 1, ih.minaddr(), ih.maxaddr()))
		return bytearray(ih.gets(ih.minaddr(), ih.maxaddr() - ih.minaddr() + 1))
	logging.info('Read from binary file "{0}"'.format(file_path))
	f = BinFormat()
	f.read(file_path)
	logging.info('Was readed 0x{0:X} ({0}) byte(s)'.format(len(f.data)))
	return f.data


def args_parse():
	parser = argparse.ArgumentParser(
		description='Atmel SAM-BA client tool',
		epilog='Copyright (C) Dean Camera, 2016. Victoria Danchenko, 2019.')
	parser.add_argument('-v', action='count', default=0, help='verbose level: -v, -vv')
	parser.add_argument('-p', '--port', \
		default='1' if sys.platform.startswith('win') else '0', \
		help='port; example: '+('1 or COM1' if sys.platform.startswith('win') else '0, ttyACM0, /dev/ttyACM0'))
	parser.add_argument('--autoconnect', action='store_true', help='autoconnect to device, see --autoconnect-vidpid')
	parser.add_argument('--autoconnect-vidpid', metavar='VID:PID', default='03eb:6124', help='VendorID:ProductID; default: 03eb:6124')
	parser.add_argument('--addresses', metavar='NAME=ADDRESS,..', \
		help='special identifier register addresses; example: CPUID=0xE000ED00,CHIPID=0x400E0740')
	parser.add_argument('--flash-boot', action='store_true', help='make boot from flash when work was done')
	parser.add_argument('--reset', action='store_true', help='reset chip when work was done')
	subparsers = parser.add_subparsers(dest='cmd', help='sub-command help')
	parser_read = subparsers.add_parser('parts', help='Show the supported parts list')
	parser_read = subparsers.add_parser('info', help='Read info about the chip')
	parser_read = subparsers.add_parser('read', help='Read data from the chip')
	parser_read.add_argument('-a', metavar='DEC_HEX', \
		help='start address. Default: flash start. Example: 0x400000 or 4M')
	parser_read.add_argument('-l', metavar='DEC_HEX', \
		help='length. Default: all flash. Example: 0x100 or 256 or 1k or 1M')
	parser_read.add_argument('-f', '--file', metavar='FILE_PATH', \
		help='file to read to. Default: stdout. Example: {}1.bin'.format('C:\\' if sys.platform.startswith('win') else '~/'))
	parser_write = subparsers.add_parser('write', help='Write to the chip')
	parser_write.add_argument('-a', metavar='DEC_HEX', \
		help='start address. Default: flash start. Example: 0x400000 or 4M')
	parser_write.add_argument('-l', metavar='DEC_HEX', help='length. Example: 0x100 or 256 or 1k or 1M')
	parser_write.add_argument('-f', required=True, metavar='FILE_PATH', \
		help='file to write from, explicit. Example: {0}1.bin or {0}1.hex'.format('C:\\' if sys.platform.startswith('win') else '~/'))
	parser_read = subparsers.add_parser('erase', help='Erase flash plane or entire chip')
	parser_read.add_argument('-a', metavar='DEC_HEX', \
		help='flash plane address. Default: entire chip. Example: 0x400000 or 4M')
	return parser.parse_args()


def parse_number(text):
	if not text:
		return None
	elif text.endswith('k') or text.endswith('K'):
		return int(text[:-1]) * 1024
	elif text.endswith('m') or text.endswith('M'):
		return int(text[:-1]) * 1024 * 1024
	else:
		if text.startswith('0x') or text.startswith('0X'):
			return int(text, 16)
		else:
			return int(text)


def is_int(text):
	try:
		int(text)
	except:
		return False
	return True


def number_to_text(number):
	suffixes = [ 'G', 'M', 'k' ]
	multiplier = 1024 ** len(suffixes)
	for suffix in suffixes:
		if number % multiplier == 0:
			return str(number / multiplier) + suffix


if __name__ == '__main__':
	# logging.basicConfig(level=logging.WARNING)
	args = args_parse()
	logging.basicConfig(level=[ logging.WARNING, logging.INFO, logging.DEBUG ][min(args.v, 2)])
	logging.info('START ' + datetime.now().isoformat())

	if args.autoconnect:
		import time
		import serial.tools.list_ports
		def autoconnect():
			'Waits until USB device connected'
			vid, pid = [ int(x, 16) for x in args.autoconnect_vidpid.split(':') ]
			while True:
				for p in serial.tools.list_ports.comports():
					if vid == p.vid and pid == p.pid:
						args.port = p.device
						logging.info('Found USB: {:04X}:{:04X} {}'.format(p.vid, p.pid, p.device))
						return
				time.sleep(.5)
		autoconnect()
	else:
		if sys.platform.startswith('win'):
			if is_int(args.port):
				args.port = 'COM' + args.port
		else:
			if is_int(args.port):
				args.port = '/dev/ttyACM' + args.port
			elif not args.port.startswith('/'):
				args.port = '/dev/' + args.port
	# print(args)
	# sys.exit(0)

	try:
		if args.cmd == 'parts':
			print('Supported parts:')
			parts_names = []
			for i in SAMBALoader.PartLibrary.SUPPORTED_PARTS:
				name = i.get_name() if hasattr(i, 'get_name') else i.__name__
				if name:
					parts_names.append(name)
			for i, v in enumerate(sorted(parts_names)):
				print('{:02} {}'.format(i + 1, v))
		else:
			try:
				transport = SAMBALoader.Transports.Serial(port=args.port)
			except Exception as e:
				print(e)
				sys.exit(2)
			samba = SAMBALoader.SAMBA(transport, is_usb=True)
			session = Session(samba)

			logging.info('SAMBA Version: %s' % samba.get_version())

			# chip recognition by their identifiers
			# read a special registers from chip
			if args.addresses:
				# overwrite default special registers addresses (for one or more registers)
				addresses = {}
				for register_and_address in args.addresses.split(','):
					register_name, register_address = register_and_address.split('=')
					addresses[register_name] = parse_number(register_address)
			else:
				# use default special registers addresses
				addresses = None
			chip_ids = session.get_part_identifiers(addresses)
			if args.cmd == 'info' or args.v > 0:
				print('Chip identifiers')
				for k, v in chip_ids.items():
					print(v)
			# find the part by special registers values
			part = session.set_part_by_chip_ids(chip_ids)
			if args.cmd == 'info' or args.v > 0:
				print('Discovered Part: %s' % part.get_name())
			if not part.is_tested():
				logging.warning('Selected part is currently untested')

			if args.cmd == 'info':
				print(part.get_info())

			elif args.cmd == 'read':
				if not args.a and not args.l:
					logging.info('Read all flash data')
				buff = part.read_flash(parse_number(args.a), parse_number(args.l))
				if args.file:
					save_to_file(args.file, buff)
				else:
					print(buff.decode('ascii', 'replace'))

			elif args.cmd == 'write':
				data = read_from_file(args.f)
				try:
					result = part.program_flash(data, parse_number(args.a))
				except SAMBALoader.Transports.TimeoutError:
					try:
						port_info = str(samba.transport)
					except:
						port_info = ''
					else:
						port_info = ' ({})'.format(port_info)
					print('Error while programming{}:'.format(port_info))
					print('Timeout happened'.format(port_info))
					sys.exit(1)
				except Exception as e:
					try:
						port_info = str(samba.transport)
					except:
						port_info = ''
					else:
						port_info = ' ({})'.format(port_info)
					print('Error while programming{}:'.format(port_info))
					print(e)
					sys.exit(2)
				if not result:
					print('Error while programming')
					sys.exit(2)

			elif args.cmd == 'erase':
				part.erase_chip(parse_number(args.a))

			if args.flash_boot:
				part.set_flash_boot()

			if args.reset:
				part.reset()

	except SAMBALoader.Transports.TimeoutError:
		logging.error('Timeout while waiting for data.')
		sys.exit(1)

	except SessionError as e:
		logging.error(str(e))
		sys.exit(1)
