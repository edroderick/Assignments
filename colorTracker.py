#!/usr/bin/env python

import controller_include as ci
import csv


import diff_drive
import ach
import sys
import time
from ctypes import *
import socket
import cv2.cv as cv
import cv2
import numpy as np

import actuator_sim as ser


CONTROLLER_REF_NAME  = 'controller-ref-chan'
error = ach.Channel(ci.CONTROLLER_REF_NAME)
error.flush()
controller = ci.CONTROLLER_REF()


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
height, width, depth = frame.shape
print 'H = ', height, ' W = ', width

while True:
    
    ret, frame = cap.read()
    img = frame
    
    # Convert RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Define upper and lower range of blue color in HSV
    lower_blue = np.array([0,100,100], dtype=np.uint8)
    upper_blue = np.array([20,255,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations = 5)
    dilation = cv2.dilate(erosion, kernel, iterations = 5)

    # Use findContours to get the boundry of the green blob
    contours,hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) > 0):
	cnt = contours[0]
	#Finding centroids of best_cnt and draw a circle there
	M = cv2.moments(cnt)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])
	cv2.circle(img,(cx,cy),5,(0,0,255),-1)
    
    else: #if no color seen, set error to 0
	x = 0
	y = 0 

    cv2.imshow('wctrl',img)
    
    cv2.waitKey(10)
    
    print '\nError in x & y: ', x, '\t', y
    
    # send the error to controller
    controller.x = x
    controller.y = y
    error.put(controller)
    time.sleep(.1)

   
   
#-----------------------------------------------------
#--------[ Do not edit below ]------------------------
#-----------------------------------------------------
