import time
import math
import RPi.GPIO as GPIO
from collections import defaultdict
from random import randint

# Pin Konfiguration
pinconfig = {
    "layer1": 26,
    "layer2": 24,
    "layer3": 22,
    "layer4": 18,
    "tower11": 16,
    "tower12": 12,
    "tower13": 10,
    "tower14": 8,
    "tower21": 23,
    "tower22": 21,
    "tower23": 19,
    "tower24": 15,
    "tower31": 13,
    "tower32": 11,
    "tower33": 7,
    "tower34": 5,
    "tower41": False,
    "tower42": False,
    "tower43": False,
    "tower44": 3
}

# Timing configuration
ledtime = 0.005
constantTickTime = True
tickThroughLayers = True

# LED Config
def tree(): return defaultdict(tree)
leds = tree()

def gpiosetup(pinid, val):
  print "Setting GPIO Pin " + str(pinid) + " up."

  if val != False:
    if val == "out":
      GPIO.setup(pinid, GPIO.OUT)
    elif val == "in":
      GPIO.setup(pinid, GPIO.IN)
    else:
      print "ERROR: Unknown GPIO state: " + val
  return

def getLayerName(x, y, z):
  if z < 5 and z > 0:
    return "layer" + str(z)
  else:
    print "Error while grabbing Layer name"
    return "error"

def getTowerName(x, y, z):
  if x < 5 and x > 0 and y < 5 and y > 0:
    return "tower" + str(x) + str(y)
  else:
    print "Error while grabbing Tower name"
    return "error"

def clearCube():
  for x in range(1, 5):
    for y in range(1, 5):
      for z in range(1, 5):
        leds[x][y][z] = False
  return

def resetPins():
  # set layers high (-> no voltage)
  for i in range(1, 5):
    if pinconfig["layer" + str(i)] != False:
      GPIO.output(pinconfig["layer" + str(i)], GPIO.HIGH)

  # set towers low (-> no voltage)
  for i in range(1, 5):
    for j in range(1, 5):
      if pinconfig["tower" + str(i) + str(j)] != False:
        GPIO.output(pinconfig["tower" + str(i) + str(j)], GPIO.LOW)
  return

def ledTick():
  ledsActivated = 0

  for x in range(1, 5):
    for y in range(1, 5):
      for z in range(1, 5):
        if leds[x][y][z] == True:
          # Get pins for layer and tower config
          layerpin = pinconfig[getLayerName(x, y, z)]
          towerpin = pinconfig[getTowerName(x, y, z)]

          if layerpin != False and towerpin != False:
            ledsActivated += 1

            # set tower high
            GPIO.output(towerpin, GPIO.HIGH)
            # set layer low
            GPIO.output(layerpin, GPIO.LOW)

            time.sleep(ledtime)

            # set tower low
            GPIO.output(towerpin, GPIO.LOW)
            # set layer high
            GPIO.output(layerpin, GPIO.HIGH)

  # wait for the remaining time until tick is over
  if constantTickTime:
    for i in range(ledsActivated, 64):
      time.sleep(ledtime)
  return

def layerTick():
  for z in range(1, 5):
    # get layer pin for current layer
    layerpin = pinconfig[getLayerName(0, 0, z)]

    # set layer low
    GPIO.output(layerpin, GPIO.LOW)

    for x in range(1, 5):
      for y in range(1, 5):
        # Get pins for tower config
        towerpin = pinconfig[getTowerName(x, y, z)]

        if layerpin != False and towerpin != False and leds[x][y][z] == True:
          # set tower high
          GPIO.output(towerpin, GPIO.HIGH)

    time.sleep(ledtime)

    for x in range(1, 5):
      for y in range(1, 5):
        # Get pins for tower config
        towerpin = pinconfig[getTowerName(x, y, z)]

        if layerpin != False and towerpin != False and leds[x][y][z] == True:
          # set tower low
          GPIO.output(towerpin, GPIO.LOW)

    # set layer high
    GPIO.output(layerpin, GPIO.HIGH)
  return

def setLedState(x, y, z, val):
  leds[x][y][z] = val
  return

def setup():
  # use RPi.GPIO Layout (with pin numbers)
  GPIO.setmode(GPIO.BOARD)

  # Save led states
  clearCube() # create led variable array and reset leds

  # Setup pins
  for i in range(1, 5): # layers
    if pinconfig["layer" + str(i)] != False:
      gpiosetup(pinconfig["layer" + str(i)], "out")

  for i in range(1, 5): # towers
    for j in range(1, 5):
      if pinconfig["tower" + str(i) + str(j)] != False:
        gpiosetup(pinconfig["tower" + str(i) + str(j)], "out")

  resetPins()

def waitTicks(ticks):
  for i in range(0, ticks):
    if tickThroughLayers:
      layerTick()
    else:
      ledTick()


# FORMS
def formLine(x1, y1, z1, x2, y2, z2):
  if x2 != x1:   # Line goes into x direction
    for x in range(x1, x2 + 1):
      setLedState(x, y1, z1, True)
  elif y2 != y1: # line goes into y direction
    for y in range(y1, y2 + 1):
      setLedState(x1, y, z1, True)
  elif z2 != z1: # line goes into z direction
    for z in range(z1, z2 + 1):
      setLedState(x1, y1, z, True)
  return

def formRect(x1, y1, z1, x2, y2, z2):
  corner1 = [x1, y1, z1]
  corner2 = [x2, y2, z1]
  corner3 = [x1, y1, z2]
  corner4 = [x2, y2, z2]

  formLine(corner1[0], corner1[1], corner1[2], corner2[0], corner2[1], corner2[2])
  formLine(corner2[0], corner2[1], corner2[2], corner3[0], corner3[1], corner3[2])
  formLine(corner3[0], corner3[1], corner3[2], corner4[0], corner4[1], corner4[2])
  formLine(corner4[0], corner4[1], corner4[2], corner1[0], corner1[1], corner1[2])
  return

def formCube(x1, y1, z1, x2, y2, z2):
  corner1 = [x1, y1, z1]
  corner2 = [x2, y1, z1]
  corner3 = [x1, y2, z1]
  corner4 = [x2, y2, z1]
  corner5 = [x1, y1, z2]
  corner6 = [x2, y1, z2]
  corner7 = [x1, y2, z2]
  corner8 = [x2, y2, z2]

  formRect(corner1[0], corner1[1], corner1[2], corner6[0], corner6[1], corner6[2])
  formRect(corner5[0], corner5[1], corner5[2], corner8[0], corner8[1], corner8[2])
  formRect(corner3[0], corner3[1], corner3[2], corner8[0], corner8[1], corner8[2])
  formRect(corner1[0], corner1[1], corner1[2], corner4[0], corner4[1], corner4[2])
  formRect(corner1[0], corner1[1], corner1[2], corner7[0], corner7[1], corner7[2])
  formRect(corner2[0], corner2[1], corner2[2], corner8[0], corner8[1], corner8[2])
  return



# ANIMATIONS
def randomize(ledsAtOnce, ticksBetweenChange, duration):
  clearCube()

  for i in range(0, duration / ticksBetweenChange):
    claerCube()
    ledsLeft = ledsAtOnce
    while ledsLeft:
      randx = randint(1, 4)
      randy = randint(1, 4)
      randz = randint(1, 4)

      if leds[randx][randy][randz] == False:
        ledsLeft -= 1
        leds[randx][randy][randz] = True

    ledsLeft = ledsAtOnce
    waitTicks(ticksBetweenChange)

  clearCube()

def testrun(runs, timePerLed):
  clearCube()

  for i in range(0, runs):
    x = 0
    y = z = 1

    running = True
    while running:
      x += 1

      if x > 4:
        x = 1
        y += 1

        if y > 4:
          y = 1
          z += 1

          if z > 4:
            running = False

      setLedState(x, y, z, True)
      waitTicks(timePerLed)
      setLedState(x, y, z, False)

  clearCube()