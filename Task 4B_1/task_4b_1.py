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
nodes=0
temp=0
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
    img_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv',img_hsv)
    # print(img_hsv[109][320])
    low_b_y=np.uint8([20,248,250])
    high_b_y=np.uint8([26,253,255])
    mask_yellow=cv2.inRange(img_hsv,low_b_y,high_b_y)
    cv2.imshow('mask_yellow',mask_yellow)
    
    contours_y,_=cv2.findContours(mask_yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # print('start')
    counter=0
    for contour in contours_y:
        approx=cv2.approxPolyDP(contour,0.1*cv2.arcLength(contour,True),True)
        cv2.drawContours(image,[approx],0,(0,0,255),5)
        counter=counter+len(approx)
        # print(len(approx))
    print(counter)

    if counter>=600 and temp==0:
        print("Node_detected")
        #stop
        nodes=nodes+1
        temp=1
    elif counter==0 and temp==1:
        temp=0
        if nodes==2:
            #left
            pass
        elif nodes==4:
            #right
            pass
        elif nodes==5:
            #left
            pass
        elif nodes==6:
            #stop
            
            pass

    previous_error=move_bot("straight",error,previous_error)
    ##########################################################

kp=0.6
kd=0
def move_bot(s,error,previous_error):
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
    left=50
    right=50
    ##################	ADD YOUR CODE HERE	##################
    if s=="stop":
        pass
    elif s=="straight":
        P=error*kp
        D=error-previous_error
        pid_value=P+kd*D
        
        L_MOTOR1.ChangeDutyCycle(left-pid_value)
        R_MOTOR1.ChangeDutyCycle(right-pid_value)

        return error
        # pass
    elif s=="left":
        
        pass
    elif s=="right":
        pass
    


################# ADD UTILITY FUNCTIONS HERE #################
L_PWM_PIN1=38
L_PWM_PIN2=40
R_PWM_PIN2=32
R_PWM_PIN1=33
enable_1=31
enable_2=37
def motor_pin_setup():
    global L_MOTOR1,L_MOTOR2,R_MOTOR1,R_MOTOR2
    GPIO.setup(R_PWM_PIN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(R_PWM_PIN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(enable_1,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(enable_2,GPIO.OUT,initial=GPIO.HIGH)

    L_MOTOR1=GPIO.PWM(L_PWM_PIN1,100)
    R_MOTOR1=GPIO.PWM(R_PWM_PIN1,100)
    L_MOTOR2=GPIO.PWM(L_PWM_PIN2,100)
    R_MOTOR2=GPIO.PWM(R_PWM_PIN2,100)
    L_MOTOR1.start(0)
    R_MOTOR1.start(0)
    L_MOTOR2.start(0)
    R_MOTOR2.start(0)


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
