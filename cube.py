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

for i in range(0, 5):
timing = 10
	formCube(1, 1, 4, 3, 4, 4)
	waitTicks(timing)
	formCube(1, 1, 3, 3, 4, 4)
	waitTicks(timing)
	formCube(1, 1, 2, 3, 4, 4)
	waitTicks(timing)
	formCube(1, 1, 1, 3, 4, 4)
	waitTicks(timing)
	formCube(1, 1, 1, 3, 3, 4)
	waitTicks(timing)
	formCube(1, 1, 1, 3, 2, 4)
	waitTicks(timing)
	formCube(1, 1, 1, 3, 1, 4)
	waitTicks(timing)
	formCube(1, 1, 2, 3, 1, 4)
	waitTicks(timing)
	formCube(1, 1, 3, 3, 1, 4)
	waitTicks(timing)
	formCube(1, 1, 4, 3, 1, 4)
	waitTicks(timing)
	formCube(1, 1, 4, 3, 2, 4)
	waitTicks(timing)
	formCube(1, 1, 4, 3, 3, 4)
	waitTicks(timing)


randomize(3, 5, 100)

GPIO.cleanup()

print "done."