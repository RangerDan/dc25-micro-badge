# DEFCON 25 micro:badge
Independent Badge for DEFCON 25 developed on the BBC micro:bit platform.  A collaboration of /r/defcon.  Runs MicroPython

- Install the uflash utility: https://uflash.readthedocs.io/en/latest/
- Install micropython runtime
- Upload badge.py using `uflash`

# Usage

- On startup, displays '/r/defcon' and a skull animation

# Future Dev

- Pair with friends running micro:badge
- Uses BTLE and sensors for Pairing and creating a persistent pager network.
- Mesh network of micro-badges repeating pages to extend range
- micro:badge on other BTLE platforms
- Listening post/repeater/logger for analyzing traffic

# Pairing

A micro:badge will not respond to a pageTwo micro:badges can pair by exchaning serial numbers.  A side-channel is used to authenticate presence of a micro:bit before it saves the serial number to the file system.

TBD

# Paging

TBD

# Updating

Before flashing new firmware, copy your paired serial numbers from your micro:bit to your host machine.  If you do not do this step, paired serial numbers will be overwritten when you upload a new script.  

Paired serial numbers are written to the flat file system of the micro:bit.  They can be dumped using the a utility that interacts with the micro:bit file system, `ufs`

TBD
