# lukas, simon, gennaro

import time
import math
import RPi.GPIO as GPIO
from collections import defaultdict
from random import randint
from cubecore import *
from cubeconfig import *

def tree(): return defaultdict(tree)

print "starting script."

setup()

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
waitTicks(100)

GPIO.cleanup()

print "done."