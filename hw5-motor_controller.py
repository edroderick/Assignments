#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2014, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */

import controller_include as ci
import dTheta_include as di
import ach
import sys
import time
import numpy as np
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
c = ach.Channel(ci.CONTROLLER_REF_NAME)
d = ach.Channel(di.CONTROLLER_REF_NAME)
d.flush()
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
controller = ci.CONTROLLER_REF()
thetacontroller = di.CONTROLLER_REF()

#gains
kp = .005
#kd = 1
#ki = 1

#initilize integral gain as zero
I = 0	
D = 0

# Get the current feed-forward (state) 
while (True):
	[status, framesize] = d.get(thetacontroller, wait=True, last=True)

	error_x = thetacontroller.dTheta
	P = kp * error_x
#	D = ki * (error1_x - error_x)/T
#	I = I + error_x

	dTheta = P + D + I

	#if error is positive, turn to the right by a factor of dTheta
	#if (dTheta > 0):
	controller.mot1 = dTheta
	controller.mot2 = -1*dTheta
        '''
	#if error is negative, turn to the left by a factor of dTheta
	if (dTheta > 0):
	    controller.mot1 = -1*dTheta
	    controller.mot2 = dTheta
        '''

	# negative values correspond to no color seen. Will not move. Overrides any previously assigned values
        if (thetacontroller.error_x == -1) and (thetacontroller.error_y == -1):
	    controller.mot1 = 0
	    controller.mot2 = 0

        print controller.mot1
        print controller.mot2
	c.put(controller)


