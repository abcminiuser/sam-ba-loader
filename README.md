# Python SAM-BA Loader

This is an implementation of a SAM-BA client for Atmel SAM devices (such as
the ATSAMD20J18A) that run either a ROM implementation of the Atmel SAM-BA bootloader, or a pre-programmed SAM-BA bootloader written to flash.

This is intended to provide an easy way to reprogram Atmel SAM devices running SAM-BA without having to use the official Atmel client (which is complex, as it is aimed primarily at the Atmel MPUs rather than MCUs). It is similar in aim to the [BOSSA](http://www.shumatech.com/web/products/bossa) software, except this client should be more generic and support a wider range of Atmel devices.

## Dependencies

Requires Python 2.7 or 3.x. So Linux, Win and Mac OSs working supported.

From a fresh Python install, use:
```
pip install pyserial
pip install xmodem
pip install IntelHex
```
Before running the tool for the first time to install the required libraries.

## Status

This fork of SAM-BA Loader can read out the identification registers of CHIPID parts (SAM3, SAM4) and DSU parts (SAMC, SAMD, SAML).

List of supported chips can be viewed by `parts` command:
```
python SAMBALoader.py parts
Supported parts:
01 ATSAM4S16B
02 ATSAM4S16C
03 ATSAM4S2A
04 ATSAM4S2B
05 ATSAM4S2C
06 ATSAM4S4A
07 ATSAM4S4B
08 ATSAM4S4C
09 ATSAM4S8B
10 ATSAM4S8C
11 ATSAM4SA16B
12 ATSAM4SA16C
13 ATSAM4SD16B
14 ATSAM4SD16C
15 ATSAM4SD32B
16 ATSAM4SD32C
17 ATSAMC
18 ATSAMD
19 ATSAML
```

The SAM4S series with Enhanced Embedded Flash Controller (EEFC) are currently supported.

The SAM C, D and L series with NVMCTRL Flash controller are currently supported.

Also, some peripheral will supported as Reset Controller (RSTC). And this list of supported peripheral can be expanded as needed to working with connected chip by SAM-BA without writing any C/C++ code, compiling and flashing. You can add a new periphery in `SAMBALoader.Peripheral` folder and use it to test Your electrical schematic using SAM-BA feature just from PC.

## Usage

SAM-BA Loader can be used as full featured command line tool or Python API.

Command line help example (Linux serial port names are shown):
```
python SAMBALoader.py -h
usage: SAMBALoader.py [-h] [-v] [-p PORT] [--addresses NAME=ADDRESS,..]
                      [--flash-boot] [--reset]
                      {parts,info,read,write,erase} ...

Atmel SAM-BA client tool

positional arguments:
  {parts,info,read,write,erase}
                        sub-command help
    parts               Show the supported parts list
    info                Read info about the chip
    read                Read data from the chip
    write               Write to the chip
    erase               Erase flash plane or entire chip

optional arguments:
  -h, --help            show this help message and exit
  -v                    verbose level: -v, -vv
  -p PORT, --port PORT  port; example: 0, ttyACM0, /dev/ttyACM0
  --addresses NAME=ADDRESS,..
                        special identifier register addresses; example:
                        CPUID=0xE000ED00,CHIPID=0x400E0740
  --flash-boot          make boot from flash when work was done
  --reset               reset chip when work was done

Copyright (C) Dean Camera, 2016. Victoria Danchenko, 2018.
```

Part can be identify by special registers (chip ID) values. This registers can be read out and has known addresses.

Information about connected device can be viewed by command line. Next example shows three `info` commands (the last is more verbose) for two devices (`15SKLCC20024020` and `18S2YQ302032002`):
```
python SAMBALoader.py info
Chip identifiers
CPUID @ 0xE000ED00: 0x410FC241
        Implementer:    ARM
        Architecture:   ARMv7-M
        Version:        r0p1
        Part:           Cortex-M3/Cortex-M4
CHIPID @ 0x400E0740: 0x29A70CE0
        Version:        0
        Processor:      Cortex-M4
        Architecture:   154 (0x9A) (Unknown)
        Flash Bank 0:   1024KB
        Flash Bank 1:   NONE
        SRAM:           160KB
        Extended ID:    0
Discovered Part: ATSAM4SD16C
Flash info
GPNVM bits: 0
Unique identifier area: 15SKLCC20024020
Descriptor: [984881, 524288, 512, 1, 524288, 64, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 9, 10, 16, 16, 96, 128, 128, 128, 128, 128, 128, 128]

python SAMBALoader.py info
Chip identifiers
CPUID @ 0xE000ED00: 0x410FC241
        Implementer:    ARM
        Architecture:   ARMv7-M
        Version:        r0p1
        Part:           Cortex-M3/Cortex-M4
CHIPID @ 0x400E0740: 0x29A70CE0
        Version:        0
        Processor:      Cortex-M4
        Architecture:   154 (0x9A) (Unknown)
        Flash Bank 0:   1024KB
        Flash Bank 1:   NONE
        SRAM:           160KB
        Extended ID:    0
Discovered Part: ATSAM4SD16C
Flash info
GPNVM bits: 0
Unique identifier area: 18S2YQ302032002
Descriptor: [984881, 524288, 512, 1, 524288, 64, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 9, 10, 16, 16, 96, 128, 128, 128, 128, 128, 128, 128]

python SAMBALoader.py -v info
INFO:root:START 2018-12-15T14:19:18.961299
INFO:SAMBALoader.Transports.Serial:Open /dev/ttyACM0 @ 115200 8N1
INFO:root:SAMBA Version: v1.11 Dec  6 2011 09:16:35
Chip identifiers
CPUID @ 0xE000ED00: 0x410FC241
        Implementer:    ARM
        Architecture:   ARMv7-M
        Version:        r0p1
        Part:           Cortex-M3/Cortex-M4
CHIPID @ 0x400E0740: 0x29A70CE0
        Version:        0
        Processor:      Cortex-M4
        Architecture:   154 (0x9A) (Unknown)
        Flash Bank 0:   1024KB
        Flash Bank 1:   NONE
        SRAM:           160KB
        Extended ID:    0
Discovered Part: ATSAM4SD16C
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A00000D
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FRR @ 0x400E0A0C: 0x00000000
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A00000E
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A00000F
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A000000
Flash info
GPNVM bits: 0
Unique identifier area: 18S2YQ302032002
Descriptor: [984881, 524288, 512, 1, 524288, 64, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 9, 10, 16, 16, 96, 128, 128, 128, 128, 128, 128, 128]
```

More devices can be supported by special registers addresses delivered in command line:
```
python SAMBALoader.py --addresses CPUID=0xE000ED00,CHIPID=0x400E0740,DSU=0x41002000
```

SAM-BA Loader Python API usage:
```
transport = SAMBALoader.Transports.Serial(port='/dev/ttyACM0')
samba = SAMBALoader.SAMBA(transport, is_usb=True)
# read special registers (chip ID) to match a part
addresses = {
	'CPUID' : 0xE000ED00,
	'CHIPID' : 0x400E0740,
	'DSU' : 0x41002000,
	}
chip_ids = SAMBALoader.PartLibrary.get_chip_ids(samba, addresses) # or .get_chip_ids(samba) if special registers addresses is known by SAM-BA Loader
# get matched parts by chip ID registers values
matched_parts = SAMBALoader.PartLibrary.find_by_chip_ids(chip_ids)
if len(matched_parts) == 1:
	# one part found
	# create part class instance
	part = matched_parts[0](samba)
	part.program_flash(data, address) # or .part.program_flash(data) if programming from flash start address
```

## License

Released under a MIT license, see README.txt.
