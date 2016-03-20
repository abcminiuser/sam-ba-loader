# Python SAM-BA Loader

This is an implementation of a SAM-BA client for Atmel SAM devices (such as
the ATSAMD20J18A) that run either a ROM implementation of the Atmel SAM-BA bootloader, or a pre-programmed SAM-BA bootloader written to flash.

This is intended to provide an easy way to reprogram Atmel SAM devices running SAM-BA without having to use the official Atmel client (which is complex, as it is aimed primarily at the Atmel MPUs rather than MCUs). It is similar in aim to the [BOSSA](http://www.shumatech.com/web/products/bossa) software, except this client should be more generic and support a wider range of Atmel devices.


## Dependencies

Python 2.x should work, Python 3.x currently untested. Requires the popular `serialport` library.


## Status

Currently the core is still in development, but it can read out the identification registers of CHIPID parts (SAM3, SAM4, SAMV, SAMS) and DSU parts (SAMD, SAMC, SAML).

The SAMD20 is currently supported for flash programming and verification. More devices will be added once the core APIs are stable.


## Use

TBA, the core implementation is not yet finished, thus the front-end is basically just a wrapper around the internal APIs for now.


## License

Released under a MIT license, see README.txt.
