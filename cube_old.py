import time
import RPi.GPIO as GPIO
from collections import defaultdict

def tree(): return defaultdict(tree)

print "starting script."

# VARIABLES

# Pin Konfiguration
pinconfig = {
    "layer1": 7,
    "layer2": 8,
    "layer3": 25,
    "layer4": 24,
    "tower11": 23,
    "tower12": 18,
    "tower13": 15,
    "tower14": 14,
    "tower21": 11,
    "tower22": 9,
    "tower23": 10,
    "tower24": 22,
    "tower31": 27,
    "tower32": 17,
    "tower33": 4,
    "tower34": 3,
    "tower41": 2,
    "tower42": false,
    "tower43": false,
    "tower44": false
}

# Timing configuration
# ledtime: Zeit, die eine LED am Stück leuchtet
ledtime = 0.005 # 5ms


# METHODS
def gpiosetup(pinid, val):
  if val != false:
    GPIO.setup(pinid, val == "out" ? GPIO.OUT : GPIO.IN)
  return

def getLayerName(x, y, z):
  if z < 5 and z > 0:
    return "layer" + z
  else:
    return "error"

def getTowerName(x, y, z):
  if x < 5 and x > 0 and y < 5 and y > 0:
    return "layer" + x + z
  else:
    return "error"

def resetLedConfig():
  for x in range(1, 5):
    for y in range(1, 5):
      for z in range(1, 5):
        leds[x][y][z] = false
  return

def resetPins():
  # set layers high (-> no voltage)
  for i in range(1, 5):
    GPIO.output(pinconfig["layer" + i], GPIO.HIGH)

  # set towers low (-> no voltage)
  for i in range(1, 5):
    for j in range(1, 5):
      GPIO.output("tower" + i + j, GPIO.LOW)
  return

def ledTick():
  for x in range(1, 5):
    for y in range(1, 5):
      for z in range(1, 5):
        if(leds[x][y][z]):
          # Get pins for layer and tower config
          layerpin = pinconfig[getLayerName(x, y, z)]
          towerpin = pinconfig[getTowerName(x, y, z)]

          # set tower high
          GPIO.output(towerpin, GPIO.HIGH)
          # set layer low
          GPIO.output(layerpin, GPIO.LOW)

          time.sleep(ledtime)

          # set tower low
          GPIO.output(towerpin, GPIO.LOW)
          # set layer high
          GPIO.output(layerpin, GPIO.HIGH)
  return

def setLedState(x, y, z, val):
  leds[x, y, z] = val
  return



# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Save led states
leds = tree()
resetLedConfig()

# Setup pins
for i in range(1, 5): # layers
  gpiosetup(pinconfig["layer" + i], out)

for i in range(1, 5): # towers
  for j in range(1, 5):
    gpiosetup("tower" + i + j, out)

resetPins()



# Script
run = true
waitticks = 0
xled = yled = zled = 1

while run:
  if waitticks != 0:
    print "tick, waiting."
    waitticks -= 1

  else:
    print "tick, doing something."
    setLedState(xled, yled, zled, false) # turn previous led off

    xled += 1
    if xled > 4:
      xled = 1
      yled += 1

      if yled > 4:
        yled = 1
        zled += 1

        if zled > 4:
          run = false

    setLedState(xled, yled, zled, true) #turn current led off

    waitticks = 20 # wait 20 ticks

  ledTick()

print "done."