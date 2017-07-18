# DEFCON 25 micro:badge
Independent Badge for DEFCON 25 developed on the BBC micro:bit platform.  A collaboration of /r/defcon.  Runs MicroPython

- Install the uflash utility: https://uflash.readthedocs.io/en/latest/
- Install micropython runtime on your micro:bit
- Modify the handle variable
- Upload badge.py using `uflash`
- Install the microfs utility to save paired handles before updating: https://microfs.readthedocs.io/en/latest/

# Usage

- On startup, displays '/r/defcon' and a skull animation
- Hold A+B to pair with another micro:badge.  Their handle will be saved to pairings.txt

# Future Dev

- Use BTLE and sensors as a pager network: sends handle and topic to paired badges.
- Mesh network of micro-badges repeating pages to extend range
- micro:badge on other BTLE platforms
- Listening post/repeater/logger for analyzing traffic

# Pairing

A micro:badge will not respond to a page unless it has been paired.  The Two micro:badges can pair by exchanging serial numbers only in pairing mode (A+B).  The handle is saved to the file system.

# Paging

TBD

# Updating

You will lose all paired handles if you do not back them up before flashing new firmware.  This is irreversible, so ensure this has been done before updating.

1. Copy your paired serial numbers from your micro:bit to your host machine using python tool microfs (ufs on the command line).  Paired handles are written to the flat file system of the micro:bit in 'pairings.txt'.  
2. Once backed up you can flash the new badge firmware.
3. Restore your pairings with ufs put.  
3. Restart your micro:badge to read the restored handles.

Sample that lists files, gets the pairing list, cats it, and then uploads it:
```
$ ufs ls
pairings.txt
$ ufs get pairings.txt
$
$ cat pairings.txt
TheOtherHandle
RangerDan$
$
$ ufs put pairings.txt
```
