# Python SAM-BA Loader
_____________________________________________________

This is an implementation of a SAM-BA client for Atmel SAM devices (such as
the ATSAMD20J18A) that run either a ROM implementation of the Atmel SAM-BA bootloader, or a pre-programmed SAM-BA bootloader written to flash.

This is intended to provide an easy way to reprogram Atmel SAM devices running SAM-BA without having to use the official Atmel client (which is complex, as it is aimed primarily at the Atmel MPUs rather than MCUs). It is similar in aim to the [BOSSA](http://www.shumatech.com/web/products/bossa) software, except this client should be more generic and support a wider range of Atmel devices.


## 1. Dependencies

Requires Python 3.x (Linux, Windows and MacOS).

Before running the tool for the first time, install all the required dependencies via:
```
pip install -r requirements.txt
```


## 2. Status

List of supported chips can be viewed by `parts` command:
```
python SAMBALoader.py parts
Supported parts:
01 ATSAM3A4C
02 ATSAM3A8C
03 ATSAM3X4C
04 ATSAM3X4E
05 ATSAM3X8C
06 ATSAM3X8E
07 ATSAM3X8H
08 ATSAM4S16B
09 ATSAM4S16C
10 ATSAM4S2A
11 ATSAM4S2B
12 ATSAM4S2C
13 ATSAM4S4A
14 ATSAM4S4B
15 ATSAM4S4C
16 ATSAM4S8B
17 ATSAM4S8C
18 ATSAM4SA16B
19 ATSAM4SA16C
20 ATSAM4SD16B
21 ATSAM4SD16C
22 ATSAM4SD32B
23 ATSAM4SD32C
24 ATSAMC
25 ATSAMD
26 ATSAML
```

The SAM3A, SAM3X, SAM4S series with Enhanced Embedded Flash Controller (EEFC) are currently supported.

The SAM C, D and L series with NVMCTRL Flash controller are currently supported.

Also, some peripheral will supported as Reset Controller (RSTC). And this list of supported peripheral can be expanded as needed to working with connected chip by SAM-BA without writing any C/C++ code, compiling and flashing. You can add a new periphery in `SAMBALoader/Peripheral` folder and use it to test Your electrical schematic using SAM-BA feature just from PC.


## 3. Usage

SAM-BA Loader can be used as full featured command line tool or Python API.

### 3.1 Command line tool: help, program and erase

***Command line help example (Linux serial port names are shown):***
```
python SAMBALoader.py -h
usage: SAMBALoader.py [-h] [-v] [-p PORT] [--autoconnect]
                      [--autoconnect-vidpid VID:PID]
                      [--addresses NAME=ADDRESS,..] [--flash-boot] [--reset]
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
  --autoconnect         autoconnect to device, see --autoconnect-vidpid
  --autoconnect-vidpid VID:PID
                        VendorID:ProductID; default: 03eb:6124
  --addresses NAME=ADDRESS,..
                        special identifier register addresses; example:
                        CPUID=0xE000ED00,CHIPID=0x400E0740
  --flash-boot          make boot from flash when work was done
  --reset               reset chip when work was done

Copyright (C) Dean Camera, 2016. Victoria Danchenko, 2019.
```

**Programming help:**
```
python SAMBALoader.py write -h
usage: SAMBALoader.py write [-h] [-a DEC_HEX] [-l DEC_HEX] -f FILE_PATH

optional arguments:
  -h, --help    show this help message and exit
  -a DEC_HEX    start address. Default: flash start. Example: 0x400000 or 4M
  -l DEC_HEX    length. Example: 0x100 or 256 or 1k or 1M
  -f FILE_PATH  file to write from, explicit. Example: ~/1.bin or ~/1.hex
```

**Programming SAM3x8E with more verbose output (`LICENSE.txt` is for test purposes. You can program .bin or .hex files):**
```
python SAMBALoader.py -v write -f LICENSE.txt
INFO:root:START 2018-12-18T16:10:27.684290
INFO:SAMBALoader.Transports.Serial:Open /dev/ttyACM0 @ 115200 8N1
INFO:root:SAMBA Version: v1.1 Dec 15 2010 19:25:04
Chip identifiers
CPUID @ 0xE000ED00: 0x412FC230
	Implementer:	ARM
	Architecture:	ARMv7-M
	Version:	r2p0
	Part:		Cortex-M3
CHIPID @ 0x400E0940: 0x285E0A60
	Version:	0
	Processor:	Cortex-M3
	Architecture:	SAM3XxE Series (144-pin version)
	Flash Bank 0:	512KB
	Flash Bank 1:	NONE
	SRAM:		96KB
	Extended ID:	0
Discovered Part: ATSAM3X8E
INFO:root:Read from binary file "LICENSE.txt"
INFO:root:Was readed 0x448 (1096) byte(s)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash write: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A080001
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash busy
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was busy for 0.002s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080000..0x00080100] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080000..0x00080100] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A080101
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash busy
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was busy for 0.002s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080100..0x00080200] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080100..0x00080200] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A080201
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash busy
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was busy for 0.003s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080200..0x00080300] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080200..0x00080300] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A080301
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash busy
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was busy for 0.003s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080300..0x00080400] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080300..0x00080400] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A080401
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash busy
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was busy for 0.002s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080400..0x00080448] 0x48 (72)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080400..0x00080448] 0x48 (72)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was wrote for 0.076s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
```

**Programming the same file again will produce this output:**
```
python SAMBALoader.py -v write -f LICENSE.txt
INFO:root:START 2018-12-18T16:06:36.669071
INFO:SAMBALoader.Transports.Serial:Open /dev/ttyACM0 @ 115200 8N1
INFO:root:SAMBA Version: v1.1 Dec 15 2010 19:25:04
Chip identifiers
CPUID @ 0xE000ED00: 0x412FC230
	Implementer:	ARM
	Architecture:	ARMv7-M
	Version:	r2p0
	Part:		Cortex-M3
CHIPID @ 0x400E0940: 0x285E0A60
	Version:	0
	Processor:	Cortex-M3
	Architecture:	SAM3XxE Series (144-pin version)
	Flash Bank 0:	512KB
	Flash Bank 1:	NONE
	SRAM:		96KB
	Extended ID:	0
Discovered Part: ATSAM3X8E
INFO:root:Read from binary file "LICENSE.txt"
INFO:root:Was readed 0x448 (1096) byte(s)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash write: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash compare: equals, not need to write: [0x00080000..0x00080100] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash compare: equals, not need to write: [0x00080100..0x00080200] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash compare: equals, not need to write: [0x00080200..0x00080300] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash compare: equals, not need to write: [0x00080300..0x00080400] 0x100 (256)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash compare: equals, not need to write: [0x00080400..0x00080448] 0x48 (72)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash was wrote for 0.036s
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash read: [0x00080000..0x00080448] 0x448 (1096)
INFO:SAMBALoader.FlashControllers.EefcFlash:Flash verify: OK
```

**Erase entire chip:**
```
python SAMBALoader.py -v erase
INFO:root:START 2018-12-18T16:07:48.123647
INFO:SAMBALoader.Transports.Serial:Open /dev/ttyACM0 @ 115200 8N1
INFO:root:SAMBA Version: v1.1 Dec 15 2010 19:25:04
Chip identifiers
CPUID @ 0xE000ED00: 0x412FC230
	Implementer:	ARM
	Architecture:	ARMv7-M
	Version:	r2p0
	Part:		Cortex-M3
CHIPID @ 0x400E0940: 0x285E0A60
	Version:	0
	Processor:	Cortex-M3
	Architecture:	SAM3XxE Series (144-pin version)
	Flash Bank 0:	512KB
	Flash Bank 1:	NONE
	SRAM:		96KB
	Extended ID:	0
Discovered Part: ATSAM3X8E
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0A04 = 0x5A000005
INFO:SAMBALoader.FlashControllers.EefcFlash:EEFC_FCR @ 0x400E0C04 = 0x5A000005
```

### 3.2 Part recognizing: automatic & manual

SAM-BA Loader recognize a part by read out the identification registers. First the `CPUID` register read for `PartNo` field acquiring (Part number of the processor):

Registers | Series
--------- | ---------
CPUID/CHIPID | SAM3, SAM4
CPUID/DSU | SAMC, SAMD, SAML

See `SAMBALoader/PartLibrary.py` file, function `PartLibrary.get_chip_ids` for details.

Special registers can be read out since has known addresses. More devices can be supported by special registers addresses as manual delivered in command line:
```
python SAMBALoader.py --addresses CPUID=0xE000ED00,CHIPID=0x400E0740,DSU=0x41002000
```

Special registers addresses as manual delivered with Python API:
```python
# read special registers (chip ID) to match a part
addresses = {
	'CPUID' : 0xE000ED00,
	'CHIPID' : 0x400E0740,
	'DSU' : 0x41002000,
	}
chip_ids = SAMBALoader.PartLibrary.get_chip_ids(samba, addresses)
```

### 3.3 How to show information about connected device

Information about connected device can be viewed by command line.
Next example shows three `info` commands for two devices (`1 QM2N815011016` and `18S2YQ302032002`):
```
python SAMBALoader.py info
Chip identifiers
CPUID @ 0xE000ED00: 0x412FC230
	Implementer:	ARM
	Architecture:	ARMv7-M
	Version:	r2p0
	Part:		Cortex-M3
CHIPID @ 0x400E0940: 0x285E0A60
	Version:	0
	Processor:	Cortex-M3
	Architecture:	SAM3XxE Series (144-pin version)
	Flash Bank 0:	512KB
	Flash Bank 1:	NONE
	SRAM:		96KB
	Extended ID:	0
Discovered Part: ATSAM3X8E
Flash info
	GPNVM bits: 0
	Unique identifier area:  1 QM2N815011016
	Descriptor: [984640, 262144, 256, 1, 262144, 16, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 16384, 9]

python SAMBALoader.py info
Chip identifiers
CPUID @ 0xE000ED00: 0x410FC241
	Implementer:	ARM
	Architecture:	ARMv7-M
	Version:	r0p1
	Part:		Cortex-M3/Cortex-M4
CHIPID @ 0x400E0740: 0x29A70CE0
	Version:	0
	Processor:	Cortex-M4
	Architecture:	SAM4SDxC Series (100-pin version)
	Flash Bank 0:	1024KB
	Flash Bank 1:	NONE
	SRAM:		160KB
	Extended ID:	0
Discovered Part: ATSAM4SD16C
Flash info
	GPNVM bits: 0
	Unique identifier area: 18S2YQ302032002
	Descriptor: [984881, 524288, 512, 1, 524288, 64, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 8192, 9, 10, 16, 16, 96, 128, 128, 128, 128, 128, 128, 128]
```

### 3.4 SAM-BA Loader Python API usage

```python
transport = SAMBALoader.Transports.Serial(port='/dev/ttyACM0') # or .Serial(port='COM1') for Win
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
	data = bytearray() # data to write
	address = 0x0 # start address to write data
	part.program_flash(data, address) # or .part.program_flash(data) if programming from flash start address
```


## 4. Credits:

Enormous thanks to [iddq](https://github.com/iddq) for their large contribution, adding new part support and various features to the CLI.


## 5. License

Released under the [MIT license](LICENSE).
