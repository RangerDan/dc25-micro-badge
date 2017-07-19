from microbit import *
import os
import radio
import music
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
# ---------------------------------------------------------------------
# If you've paired and want to reflash your firmware, use ufs tool
# to save pairings file and restore after flashing
# ---------------------------------------------------------------------

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
    pairings = [handle]
else:
    with open('pairings.txt', 'r') as pairingsFile:
        pairings = pairingsFile.read().split(handleSeparator)

pairing = False
pairingStart = 0
pairingAnimation = [Image("50000:50000:50000:50000:50000"),
                    Image("05000:05000:05000:05000:05000"),
                    Image("00500:00500:00500:00500:00500"),
                    Image("00050:00050:00050:00050:00050"),
                    Image("00005:00005:00005:00005:00005")]

pagingAnimation = [Image("99999:99999:99999:99999:99999"),
                   Image("00000:00000:00000:00000:00000")]

# Topics
topic = 0
topics = ["Gen",
          "Chill",
          "HHV",
          "Vote",
          "Crypto",
          "Wifi",
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

# Tones for send, recieve
tuneSend = ["G4:8","C","D","G3"]
tuneReceive = ["G3:8","D4","E","C"]

# Opening Scroll/Skull
display.scroll('/r/defcon')
display.show(skull, 200, wait=False, loop=True, clear=False)
music.play(tuneSend)
music.play(["R:16"])
music.play(tuneReceive)
radio.on()
radio.config(length=64)

# Ready for action
while True:
    # default
    if not pairing and (button_a.is_pressed() or button_b.is_pressed()):
        # debounce
        sleep(150)
        if button_a.is_pressed() and button_b.is_pressed():
            display.show(pairingAnimation, 200, wait=False,
                         loop=True, clear=False)
            pairing = True
            pairingStart = running_time()
        # Move Left
        elif button_a.is_pressed():
            if topic == 0:
                topic = maxTopic
            else:
                topic = topic - 1
            display.scroll(topics[topic], delay=100, wait=True, loop=False)
            display.show(skull, 200, wait=False, loop=True, clear=False)
        # Move Right
        elif button_b.is_pressed():
            if topic == maxTopic:
                topic = 0
            else:
                topic = topic + 1
            display.scroll(topics[topic], delay=100, wait=True, loop=False)
            display.show(skull, 200, wait=False, loop=True, clear=False)

    # Pairing Mode
    if pairing:
        # Pairing...
        if running_time() < pairingStart + 10000:
            radio.send('P|'+handle)
            incoming = radio.receive()
            # Got Something?
            if incoming is not None and incoming[0] == 'P':
                newPairing = incoming[2:]
                if newPairing not in pairings:
                    pairings.append(newPairing)
                    with open('pairings.txt', 'w') as pairingsFile:
                        pairingsFile.write('\n'.join(pairings))
                    # Display the paired name
                    display.scroll(newPairing, 100, wait=True, loop=False)
                    # Turn off pairing
                    display.show(skull, 300, wait=False,
                                 loop=True, clear=False)
                    pairing = False
            # Wait and try again
            else:
                sleep(500)
        # Pairing Mode Stop
        elif pairing and running_time() >= pairingStart + 10000:
            pairing = False
            display.show(skull, 300, wait=False, loop=True, clear=False)

    # Broadcast if shaken vigorously
    if accelerometer.was_gesture('shake'):
        display.scroll(topics[topic], delay=100, wait=True, loop=False)
        for name in pairings:
            if(name != handle):
                radio.send('B|'+handle+'|'+name+'|'+topics[topic])
                music.play(tuneSend)
        display.show(skull, 300, wait=False, loop=True, clear=False)

    # Detect a page
    if not pairing:
        incoming = radio.receive()
        if incoming is not None and incoming[0] == 'B':
            page = incoming.split('|')
            if page[2] == handle and page[1] != handle and page[1] in pairings:
                display.show(pagingAnimation, 200, wait=True, loop=False, clear=False)
                display.show(pagingAnimation, 200, wait=True, loop=False, clear=False)
                display.show(pagingAnimation, 200, wait=True, loop=False, clear=False)
                music.play(tuneReceive)
                display.scroll(page[1]+'-', delay=100, wait=True, loop=False)
                display.scroll(page[3], delay=100, wait=True, loop=False)
                display.show(skull, 300, wait=False, loop=True, clear=False)
