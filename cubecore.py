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
            print "LED " + str(x) + str(y) + str(z) + " is currently on, using tower" + str(pinconfig[getTowerName(x, y, z)]) + " and layer" + str(pinconfig[getLayerName(x, y, z)])  

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
  for i in range(ledsActivated, 64):
    time.sleep(ledtime)
  return

def setLedState(x, y, z, val):
  leds[x][y][z] = val
  return

def setup():
  # use RPi.GPIO Layout (with pin numbers)
  GPIO.setmode(GPIO.BOARD)

  # Save led states
  leds = tree()
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
    ledTick()