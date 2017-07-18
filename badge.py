# DEFCON 25 micro:badge
# Badge for /r/defcon on BBC micro:bit running micropython
# By DuncanYoudaho and TrustedRoot
# A glowing skull, bluetooth pairing, and pager
# -------------------------------------------------------------------
# Step 1: Insert your handle here:
handle = 'DuncanYoudaho'
# Step 2: Install the micropython runtime to your micro:bit
# Step 3: Use uflash to flash badge.py to your micro:bit
# Step 4: Find another micro:badge and hold A+B to pair
# Step 5: Hook up headphones to GND and Pin 0
# Step 6: Send a page by choosing a topic and shaking the badge
#---------------------------------------------------------------------
# If you've paired and want to reflash your firmware, use ufs tool
# to save pairings file and restore after flashing
#---------------------------------------------------------------------
from microbit import *
import os
import radio

# Load Pairings from File
# Pairings file Syntax: 
# Handle1\n
# HackerHandle2\n
# 1337H4x0r<EOF>
handleSeparator = '\n'
pairings = []
if 'pairings.txt' not in os.listdir():
    with open('pairings.txt', 'w') as pairingsFile:
        pairingsFile.write(handle)
else:
    with open('pairings.txt', 'r') as pairingsFile:
        pairings = pairingsFile.read().split(handleSeparator)

pairing = False
pairingStart = 0
pairingAnimation = [Image("50000:50000:50000:50000:50000"),
                    Image("00500:00500:00500:00500:00500"),
                    Image("00005:00005:00005:00005:00005")]

topic = 0
topics = ["General",
          "ChillOut",
          "HHV",
          "Voting",
          "Crypto",
          "Wireless",
          "Trk1",
          "Trk2",
          "Trk3",
          "Trk4",
          "Trk5"]
maxTopic = len(topics) - 1

skull = [Image("05550:50505:55055:05550:05550"),
         Image("05550:53535:55355:05550:05550"),
         Image("05550:56565:55655:05550:05550"),
         Image("05550:53535:55355:05550:05550")]

display.scroll('/r/defcon')

display.show(skull, 200, wait=False, loop=True,clear=False)

while True:
    # default
    if not pairing and (button_a.is_pressed() or button_b.is_pressed()):
        # debounce
        sleep(150)
        if button_a.is_pressed() and button_b.is_pressed():
            display.show(pairingAnimation,200,wait=False,loop=True,clear=False)
            pairing = True
            pairingStart = running_time()
            radio.on()
        # Move Left
        elif button_a.is_pressed():
            if topic == 0:
                topic = maxTopic
            else:
                topic = topic - 1
            display.scroll(topics[topic],delay=100,wait=True,loop=False)
            display.show(skull, 200, wait=False, loop=True,clear=False)
        # Move Right
        elif button_b.is_pressed():
            if topic == maxTopic:
                topic = 0
            else:
                topic = topic + 1
            display.scroll(topics[topic],delay=100,wait=True,loop=False)
            display.show(skull, 200, wait=False, loop=True,clear=False)

    # Pairing Mode start
    if pairing and running_time() < pairingStart + 10000:    
        radio.send('P|'+handle)
        incoming = radio.receive()
        if incoming is not None and incoming[0] == 'P':
            newPairing = incoming[2:]
            if newPairing not in pairings:
                pairings.append(newPairing)
                with open('pairings.txt', 'w') as pairingsFile:
                    pairingsFile.write('\n'.join(pairings))            
                # Display the paired name
                display.scroll(newPairing,100,wait=True,loop=False)
                display.show(skull, 300, wait=False, loop=True,clear=False)
                pairing = 0
        else:
            sleep(500)
    # Pairing Mode Stop
    elif pairing and running_time() >= pairingStart + 10000:
        pairing = False
        radio.off()
        display.show(skull, 300, wait=False, loop=True,clear=False)