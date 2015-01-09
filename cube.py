# lukas, simon, gennaro

import time
import math
import RPi.GPIO as GPIO
from collections import defaultdict
from random import randint
from cubecore import *


print "starting script."

setup()

testrun(1, 10)

formCube(1, 1, 1, 3, 3, 3)
waitTicks(10)
formCube(1, 1, 1, 3, 3, 2)
waitTicks(10)
formCube(1, 1, 1, 3, 3, 1)
waitTicks(10)
formCube(1, 1, 1, 3, 3, 2)
waitTicks(10)
formCube(1, 1, 1, 3, 3, 3)
waitTicks(10)
formCube(1, 1, 1, 3, 2, 3)
waitTicks(10)
formCube(1, 1, 1, 3, 1, 3)
waitTicks(10)
formCube(1, 1, 1, 3, 2, 3)
waitTicks(10)
formCube(1, 1, 1, 3, 3, 3)
waitTicks(30)

randomize(3, 5, 100)

GPIO.cleanup()

print "done."