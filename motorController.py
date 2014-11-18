#!/usr/bin/env python

import controller_include as ci
import controller_include2 as ci2
import collections

import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np
import math


e = ach.Channel(ci.CONTROLLER_REF_NAME)
e.flush()
controller = ci.CONTROLLER_REF()

e2 = ach.Channel(ci2.DYNO_REF_NAME)
e2.flush()
controller2 = ci2.DYNO_REF()

kp = 0.012

while True:
	[statuss, framesizes] = e.get(controller, wait=True, last=True)
	x = controller.x
	y = controller.y
	print '\nErrors in X & Y is:\t', x, ',\t', y
	
	#P controller, sets output values to radians to match motor's expected input
	dThetaX = math.radians(-kp * x)
	dThetaY = math.radians(kp * y)
		
	# Command motors only if there is an error
	if ( (dThetaX != 0) | (dThetaY !=0) ):
		controller2.dThetaX = dThetaX
		controller2.dThetaY = dThetaY
		e2.put(controller2)
		print 'dTheta X & Y is: \t', dThetaX, ',\t', dThetaY
	else:
		print 'no Error detected!'
