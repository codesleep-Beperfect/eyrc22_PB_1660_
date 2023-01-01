'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
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
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################
kp=0.6
kd=0
def pid(sim,error, previous_error):
	P=error*kp
	D=error-previous_error
	pid_value=P+kd*D
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	#right velo +pid_value
	sim.setJointTargetVelocity(left,3-pid_value)
	sim.setJointTargetVelocity(right,3+pid_value)
	return error
def move_left(sim):
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(left,-1)
	sim.setJointTargetVelocity(right,1)
	time.sleep(2)

def move_right(sim):
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(left,1)
	sim.setJointTargetVelocity(right,-1)
	time.sleep(2)

def stop(sim):
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(left,0)
	sim.setJointTargetVelocity(right,0)
def dropoff(sim,checkpoint):
	message=read_qr_code(sim)
	obj_package={"Orange Cone":"package_1","Pink Cuboid":"package_3","Blue Cylinder": "package_2"}
	# print(message)
	## Retrieve the handle of the Arena_dummy scene object.
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle, obj_package[message], checkpoint)
def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############
	
	# left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	# right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	# sim.setJointTargetVelocity(left,1)
	# sim.setJointTargetVelocity(right,1)

	vision_sensor_handle=sim.getObjectHandle('/Diff_Drive_Bot/vision_sensor')
	error=0
	previous_error=0

	nodes=0
	temp=0
	while True:
		img,shape=sim.getVisionSensorImg(vision_sensor_handle)
		# print(shape)
		img=np.frombuffer(img,dtype=np.uint8).reshape(shape[0],shape[1],3)
		img=cv2.flip(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),0)
		# print(img[])
		# white 255 255 255
		#black 76 76 76 
		#light gray 198 198 198
		#medium gray 154 154 154
		#dark gray 119 119 119

		low_b=np.uint8([0,0,0])
		high_b=np.uint8([200,200,200])
		# low_b=np.uint8([88,173,193])
		# high_b=np.uint8([6,206,256])
		mask=cv2.inRange(img,low_b,high_b)
		contours,hierarchy=cv2.findContours(mask,2,cv2.CHAIN_APPROX_NONE)

		# cv2.circle(img,(253,255),5,(0,0,255),-1)
		if len(contours)>0:
			# print(len(contours))
			c=max(contours,key=cv2.contourArea)
			M=cv2.moments(c)
			if M['m00']!=0:
				cx=int(M['m10']/M['m00'])
				cy=int(M['m01']/M['m00'])
				# cv2.circle(img,(cx,cy),5,(255,255,0),-1)
				
				# print(cx,cy)
		# cx= 253 +- 35 error =0
		# cx= 218 -> 183 error =
		#cx = 183 ->148
		#cx =148 -> 113
		#
		# road width =450
		#228, 178,128,78,28
		#278,328, 378, 428, 478

		#206,180,154,128,104,77,51,25
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
			error =-4
		# R    G   B
		# 253, 204,4
		##### detecting a node############################################
		img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		# cv2.imshow('hsv',img_hsv)
		# print(img_hsv[109][320])
		low_b_y=np.uint8([20,248,250])
		high_b_y=np.uint8([26,253,255])
		mask_yellow=cv2.inRange(img_hsv,low_b_y,high_b_y)
		# cv2.imshow('mask_yellow',mask_yellow)
		
		contours_y,_=cv2.findContours(mask_yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		# print('start')
		counter=0
		for contour in contours_y:
			approx=cv2.approxPolyDP(contour,0.1*cv2.arcLength(contour,True),True)
			cv2.drawContours(img,[approx],0,(0,0,255),5)
			counter=counter+len(approx)
			# print(len(approx))
		# print(counter)

		if counter==44  and temp==0 :
			stop(sim)
			time.sleep(0.25)
			nodes=nodes+1
			temp=1
			if(nodes==5):
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint E")
				dropoff(sim, "checkpoint E")
			elif(nodes==9):
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint I")
				dropoff(sim, "checkpoint I")	
			elif(nodes==13):
				arena_dummy_handle = sim.getObject("/Arena_dummy") 
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
				sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint M")
				dropoff(sim, "checkpoint M")
		elif counter==0 and temp==1:
			if nodes==1:
				##move_left
				move_left(sim)
			elif nodes==2:
				##move_right
				move_right(sim)
			elif nodes==3:
				##move_left
				move_left(sim)
			elif nodes==4:
				#move_right
				move_right(sim)
			elif nodes==6:
				##move_right
				move_right(sim)
			elif nodes==7:
				##move_left
				move_left(sim)
			elif nodes==8:
				##move_right
				move_right(sim)
			# elif nodes==9:
			# 	##drop off
			# 	dropoff()
			elif nodes==10:
				##move_right
				move_right(sim)
			elif nodes==11:
				##move_left
				move_left(sim)
			elif nodes==12:
				##move_right
				move_right(sim)
			# elif nodes==13:
			# 	#dropoff
			# 	dropoff()
			elif nodes==14:
				##move_right
				move_right(sim)
			elif nodes==15:
				##move_left
				move_left(sim)
			elif nodes==16:
				##move_right
				move_right(sim)
			elif nodes==17:
				
				stop(sim)
				break
			temp=0
		##############################################################

		previous_error=pid(sim,error,previous_error)
		# print(nodes)
		# print('end')
		
		
		
		
		# if straight line then pid else turn right or left 
		previous_error=pid(sim,error,previous_error)

		# cv2.drawContours(img,c,-1,(0,255,0),3)
		# cv2.imshow('mask',mask)
		# cv2.imshow('image',img)

		cv2.waitKey(1)
	##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	vision_sensor_handle=sim.getObjectHandle('/Diff_Drive_Bot/vision_sensor')

	img,shape=sim.getVisionSensorImg(vision_sensor_handle)
		# print(shape)
	img=np.frombuffer(img,dtype=np.uint8).reshape(shape[0],shape[1],3)
	img=cv2.flip(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),0)
	qrs=decode(img)
	for qr in qrs:
		qr_message= qr.data.decode('UTF-8')

	# for qr in qrs_raw:
	# 	points=qr.polygon
    # 	center=[int((points[0].x+points[2].x)/2),int((points[0].y+points[2].y)/2)]
    # 	Qr_codes_details[qr.data.decode('UTF-8')]=center

	
	##############  ADD YOUR CODE HERE  ##############

	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(left,0)
	sim.setJointTargetVelocity(right,0)
	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			time.sleep(5)
			control_logic(sim)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()