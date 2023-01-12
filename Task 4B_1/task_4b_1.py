'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B-Part 1 of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b_1.py
# Functions:		control_logic, move_bot
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section.   ##
## You have to implement this task with the available modules ##
##############################################################

import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
import sys
import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera

########### ADD YOUR UTILITY FUNCTIONS HERE ##################

##############################################################

def control_logic(image):

    """
    Purpose:
    ---
    This function is suppose to process the frames from the PiCamera and
    check for the error using image processing and with respect to error
    it should correct itself using PID controller.

    >> Process the Frame from PiCamera 
    >> Check for the error in line following and node detection
    >> PID controller

    Input Arguments:
    ---
    You are free to define input arguments for this function.

    Hint: frame [numpy array] from PiCamera can be passed in this function and it can
        take the action using PID 

    Returns:
    ---
    You are free to define output parameters for this function.

    Example call:
    ---
    control_logic()
    """    

    ##################	ADD YOUR CODE HERE	##################


    ##########################################################

def move_bot():
    """
    Purpose:
    ---
    This function is suppose to move the bot

    Input Arguments:
    ---
    You are free to define input arguments for this function.

    Hint: Here you can have inputs left, right, straight, reverse and many more
        based on your control_logic

    Returns:
    ---
    You are free to define output parameters for this function.

    Example call:
    ---
    move_bot()
    """    

    ##################	ADD YOUR CODE HERE	##################
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    low_b=np.uint8([0,0,0])
    high_b=np.uint8([70,70,70])
    mask=cv2.inRange(image,low_b,high_b)
    cv2.imshow("mask",mask)
    contours,hierarchy=cv2.findContours(mask,2,cv2.CHAIN_APPROX_NONE)
    cx=0
    cy=0
		# cv2.circle(img,(253,255),5,(0,0,255),-1)
    if len(contours)>0:
        # print(len(contours))
        c=max(contours,key=cv2.contourArea)
        M=cv2.moments(c)
        if M['m00']!=0:
            cx=int(M['m10']/M['m00'])
            cy=int(M['m01']/M['m00'])

    ##########################################################
    if cx!=0 and cy!=0:
        if cx<=278 and cx>228:
            error=0
        elif cx<=228 and cx>178:
            error=1
        elif cx<=178 and cx>128:
            error =2
        elif cx<=128 and cx > 78:
            error=3
        elif cx<=78 and cx>=28:
            error=4
        elif cx>278 and cx <=328:
            error=-1
        elif cx >328 and cx <=378:
            error=-2
        elif cx>378 and cx<=428:
            error =-3
        elif cx>428 and cx<=478:
            error=-4



################# ADD UTILITY FUNCTIONS HERE #################





##############################################################
    
if __name__ == "__main__":

    """
    The goal of the this task is to move the robot through a predefied 
    path which includes straight road traversals and taking turns at 
    nodes. 

    This script is to be run on Raspberry Pi and it will 
    do the following task.
 
    >> Stream the frames from PiCamera
    >> Process the frame, do the line following and node detection
    >> Move the bot using control logic

    The overall task should be executed here, plan accordingly. 
    """    

    ##################	ADD YOUR CODE HERE	##################
    camera=PiCamera()
    camera.resolution=(512,512)
    camera.framerate=32
    rawCapture=PiRGBArray(camera,size=(512,512))#640,480
    stream=camera.capture_continuous(rawCapture,format="bgr",use_video_port=True)
    for frame in stream:
        image=frame.array
        cv2.imshow("Frame",image)
        control_logic(image)


        key=cv2.waitKey(1)& 0xFF

        rawCapture.truncate(0)

        if key==ord("q"):
            cv2.destroyAllWindows()
            break

    ##########################################################

    # pass
