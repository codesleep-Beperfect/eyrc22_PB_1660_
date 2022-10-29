'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
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
##############################################################
kp=6.33 #working fine for 6.5
kd=1.288 #working fine for 1.3
def forward(sim,left,right,distance_side,e_prev):
	if distance_side==None or (distance_side >= 0.170 and distance_side<0.180):
		sim.setJointTargetVelocity(left,2)
		sim.setJointTargetVelocity(right,2)
	else :
		delta=distance_side-0.17
		P=kp*delta
		D=kd*(delta-e_prev)
		pd=P-D
		print(e_prev)
		e_prev=delta
		sim.setJointTargetVelocity(left,2+pd)
		sim.setJointTargetVelocity(right,2-pd)

	return e_prev


def left_move(sim,left,right):
	sim.setJointTargetVelocity(left,-1)
	sim.setJointTargetVelocity(right,1)
	time.sleep(2.6)


def right_move(sim,left,right):
	sim.setJointTargetVelocity(left,1)
	sim.setJointTargetVelocity(right,-1)
	time.sleep(2.6)
def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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
	speed_left=1
	speed_right=1
	tolerance=0.001
	left=sim.getObjectHandle('/Diff_Drive_Bot/left_joint')
	right=sim.getObjectHandle('/Diff_Drive_Bot/right_joint')
	sim.setJointTargetVelocity(left,0)
	sim.setJointTargetVelocity(right,0)
	right_temp=0
	left_temp=0
	e_prev=0
	while True:
		
		distance_side=detect_distance_sensor_2(sim)
		# print(distance_side)
		distance_front=detect_distance_sensor_1(sim)
		# print(distance_front)
		if distance_front==None:
			e_prev=forward(sim,left,right,distance_side,e_prev)
			print(e_prev)
			left_temp=0
			right_temp=0
			# print('right')
		elif (distance_front<=0.22 ) and distance_side!=None:
			left_move(sim,left,right)
			left_temp=1
			print('left')
		elif (distance_front<=0.22 ) and distance_side==None:
			right_move(sim,left,right)
			print("right")

	##############  ADD YOUR CODE HERE  ##############
	
	# while True:
	# 	distance_side=detect_distance_sensor_2(sim)
	# 	distance_front=detect_distance_sensor_1(sim)
	# 	print(distance_side)
	# 	if(distance_side is not None):
	# 		speed_left=speed_left-(0.17-distance_side)*0.75
	# 		speed_right=speed_right+(0.17-distance_side)*0.75
		
	# 	sim.setJointTargetVelocity(left,speed_left)
	# 	sim.setJointTargetVelocity(right,speed_right)




	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None

	##############  ADD YOUR CODE HERE  ##############
	sensor1=sim.getObjectHandle('/distance_sensor_1')
	
	temp=sim.readProximitySensor(sensor1)
	if temp[0]:
		distance= temp[1]
	



	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None

	##############  ADD YOUR CODE HERE  ##############
	sensor2=sim.getObjectHandle('/Diff_Drive_Bot/distance_sensor_2')
	temp=sim.readProximitySensor(sensor2)
	if temp[0]:
		distance= temp[1]
		



	##################################################
	return distance
def detect_distance_sensor_3(sim):
	distance = None

	##############  ADD YOUR CODE HERE  ##############
	sensor3=sim.getObjectHandle('/distance_sensor_3')
	
	temp=sim.readProximitySensor(sensor3)
	if temp[0]:
		distance= temp[1]
	



	##################################################
	return distance


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')
	

	
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
			control_logic(sim)
			time.sleep(5)

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