#reverse vali condition 
#bot slow
#define 4 values of nodes min and max
#camera fps increase using multithreading 
'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''
##Problems that we are facing
'''
frame freezes as soon as node is detected
input message not receiving in correct format. 
expected -: 
Node 
Node 
NONODE
Message Received-:
NodeNodeNONODE
'''
# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy
import cv2
from pyzbar.pyzbar import decode
import json
import random
from threading import Thread
import threading
import math	
from cv2 import aruco
##############################################################

## Import PB_theme_functions code
try:
	pb_theme = __import__('PB_theme_functions')

except ImportError:
	print('\n[ERROR] PB_theme_functions.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure PB_theme_functions.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your PB_theme_functions.py throwed an Exception, kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


###############################################******************************************************************************************
x1=-10
y1=-10
x2=-10
y2=-10
x3=-10
y3=-10
x4=-10
y4=-10
tl=()
tr=()
bl=()
br=()
def perspective_transform(image):
    global x1,y1,x2,y2,x3,y3,x4,y4,tl,tr,bl,br
    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = []
    Aruco_details,Aruco_corners=pb_theme.detect_ArUco_details(image) 
    if(x1==-10 and y1==-10):
        if Aruco_details.get(1):
            #br
            x1=Aruco_details[1][0][0]
            y1=Aruco_details[1][0][1]
            tl=(x1,y1)
    if(x2==-10 and y2==-10):
        if Aruco_details.get(2):
            #bl
            x2=Aruco_details[2][0][0]
            y2=Aruco_details[2][0][1]
            tr=(x2,y2)
    if(x3==-10 and y3==-10):
        if Aruco_details.get(3):
            #tl
            x3=Aruco_details[3][0][0]
            y3=Aruco_details[3][0][1]
            br=(x3,y3)
    if(x4==-10 and y4==-10):
        
        if Aruco_details.get(4):
            #tr
            x4=Aruco_details[4][0][0]
            y4=Aruco_details[4][0][1]  
            bl=(x4,y4)  
    if x1!=-10 and x2!=-10 and x3!=-10 and x4!=-10:
        # print(Aruco_details[1][0])
        pts1=numpy.float32([tl,bl,tr,br])
        pts2=numpy.float32([[0,0],[0,440],[410,0],[410,440]])
        matrix=cv2.getPerspectiveTransform(pts1,pts2)
        warped_image=cv2.warpPerspective(image,matrix,(410,440))
        # cv2.imshow('transformed_frame',transformed_frame)

    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []

    Aruco_details1,Aruco_corners1=pb_theme.detect_ArUco_details(image)
    # task_1b.mark_ArUco_image(frame,Aruco_details1, Aruco_corners1)
    # cv2.imshow('marked',frame)
    # print(Aruco_details)
    if Aruco_details1.get(5):
        x_pixel=Aruco_details1[5][0][0]
        y_pixel=Aruco_details1[5][0][1]
        # print(x_pixel,y_pixel)
        y_cop=0.0044*y_pixel-0.9787+0.03
        pixel_per_cm=103.85*y_cop*y_cop*y_cop*y_cop*y_cop-5.0625*y_cop*y_cop*y_cop*y_cop-81.685*y_cop*y_cop*y_cop-4.182*y_cop*y_cop+9.8966*y_cop+210.86
        x_cop=(215-x_pixel)*1.0/pixel_per_cm-0.05
        # print(x_cop,y_cop)

        angle_image=Aruco_details1[5][1]
        # angle_cop=0
        # if angle_image>0:
        #     angle_cop=180-angle_image
        # if angle_image<=0:
        #     angle_cop=angle_image+180
        # print(angle_image,angle_cop)
        scene_parameters.append(x_cop)
        scene_parameters.append(y_cop)
        scene_parameters.append(angle_image)
    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    
    aruco_handle = sim.getObject('/aruco_5')
    aruco_handle_3=sim.getObject('/Arena')

    if len(scene_parameters):
        sim.setObjectPosition(aruco_handle,aruco_handle_3,[scene_parameters[0],scene_parameters[1],0])
        # if( scene_parameters[2]<=90):
        #     alpha=(90-scene_parameters[2])*0.0175
        # else :
        #     alpha=(scene_parameters[2]-90)*0.0175
        # print(scene_parameters[2])
        angle_rad=scene_parameters[2]*0.0175
        sim.setObjectOrientation(aruco_handle,sim.handle_world,[0,0,angle_rad])

    return None

########################################################################*****************************************************************

			
def code_moves(path_to_moves):
	final=""
	for move in path_to_moves:
		if move=="STRAIGHT":
			final=final+"S_"
		elif move=="LEFT":
			final=final+"L_"
		elif move=="RIGHT":
			final=final+"R_"
		elif move=="REVERSE":
			final=final+"RV_"
		elif move=="WAIT_5":
			final=final+"W5_"
	return final

def target_reached(a_x,a_y):
	#x_min_e4 y_max_e4 y_min_e4 y_max_e4
	x_min_e4=0.5192
	x_max_e4=0.6592
	y_max_e4=-0.04809
	y_min_e4=-0.0900

	#x_min_e5 y_max_e5 y_min_e5 y_max_e5
	x_min_e5=0.5062
	x_max_e5=0.6662
	y_min_e5=-0.5095
	y_max_e5=-0.3495
	if a_x>=x_min_e4 and a_x<=x_max_e4 and a_y>=y_min_e4 and a_y<=y_max_e4:
		return True
	if a_x>=x_min_e5 and a_x<=x_max_e5 and a_y>=y_min_e5 and a_y<=y_max_e5:
		return True
	return False
def task_4b_implementation(sim,config_image,start_node,end_node,traffic_signals,connection):
	"""
	Purpose:
	---
	This function contains the implementation logic for task 4B 

	Input Arguments:
	---
    `sim` : [ object ]
            ZeroMQ RemoteAPI object

	You are free to define additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	task_4b_implementation(sim)
	"""

	##################	ADD YOUR CODE HERE	##################
	x_min=0.7871
	x_max=0.9472
	y_min=0.4261
	y_max=0.5361
	target_nodes=[start_node,"F2",end_node]
	graph=pb_theme.detect_paths_to_graph(config_image)
	i=1
	backtrace_path=pb_theme.path_planning(graph,start_node,"F2")
	path_to_moves=pb_theme.paths_to_moves(backtrace_path,traffic_signals)
	moves_code=code_moves(path_to_moves)
	pb_theme.send_message_via_socket(connection,moves_code)

	cap = cv2.VideoCapture(0)

	counter=0
	counterf2=0
	while True:
		ret, frame = cap.read()
		cv2.imshow('frame',frame)
		if cv2.waitKey(100) & 0xFF == ord('q'):
			break
		frame=frame[40:,100:510]
		
		cameraMatrix=numpy.array([[669.2721006 ,   0.    ,     308.27537125],
[  0.      ,   664.83129387 ,268.35372325],
[  0.,           0.  ,         1.  ,      ]])
		dist=numpy.array([[-7.77722198e-01 , 2.17364635e-02, -7.01392560e-04 , 5.27929722e-03,
1.30080094e+00]])
		h,  w = frame.shape[:2]
		newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
		dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
		t=perspective_transform(dst)

		if len(t):
			
			a=transform_values(t)
			#print(a)
			set_values(a)
		#check only for f2 predefine four values xmin xmax, ymin ymax
		#counter=1 when f2 is detected#inside f2 block
		#decrypt message in f2  condition#inside f2 block 
		#update target node according to decrypted message# inside f2 block
		#check value of counter - if counter is one -
		#											startnode= target[i] endnode=target[i+1] increment value of i 
		#											pathplanning and backtrace path
		#											send message to raspi
		#											if i == len(target nodes)-1 :break
			if a:
				a_x=a[0]
				a_y=a[1]
				if x_min<=a_x and x_max>=a_x and y_min<=a_y and y_max>=a_y and counterf2==0:
					counter = 1 
					counterf2=1
					# message decryption 
					print("Line no 370")
					copp_message={ "Pink_Cone":"E4","Orange_Cone":"E5"}
					for node in copp_message.values():
						target_nodes.insert(-1,node)
					print(target_nodes)
					colour_string=""
					for colour in copp_message:
						colour=colour.split("_")
						colour_string=colour_string+colour[0]+"_"
					
					pb_theme.send_message_via_socket(connection,colour_string)

				# target_reached(ax,ay) return True for reached and false for not reached -:
				#																			if reached counter=1
				if target_reached(a_x,a_y):
					print("Line no. 377")
					counter=1


				if counter:
					print("Line no. 382")
					counter=0
					start=target_nodes[i]
					end=target_nodes[i+1]
					print("start_node ",start)
					print("End node ",end)
					
					i=i+1
					backtrace_path=pb_theme.path_planning(graph,start,end)
					path_to_moves=pb_theme.paths_to_moves(backtrace_path,traffic_signals)
					print(backtrace_path)
					moves_code=code_moves(path_to_moves)
					print(path_to_moves)
					pb_theme.send_message_via_socket(connection,moves_code)
					if i==len(target_nodes)-1:
						print("Line no. 390")
						break
				


				##########################################################
	
	cap.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	
	host = ''
	port = 5050


	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()


	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		pass
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()

	# ## Set up new connection with Raspberry Pi
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()

	## Send setup message to PB_socket
	pb_theme.send_message_via_socket(connection_1, "SETUP")

	message = pb_theme.receive_message_via_socket(connection_1)
	## Loop infinitely until SETUP_DONE message is received
	while True:
		if message == "SETUP_DONE":
			break
		else:
			print("Cannot proceed further until SETUP command is received")
			message = pb_theme.receive_message_via_socket(connection_1)

	try:
		# obtain required arena parameters
		config_img = cv2.imread("config_image.png")
		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)			
		medicine_package_details = detected_arena_parameters["medicine_packages"]
		traffic_signals = detected_arena_parameters['traffic_signals']
		start_node = detected_arena_parameters['start_node']
		end_node = detected_arena_parameters['end_node']
		horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
		vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']
		
		# print("Medicine Packages: ", medicine_package_details)
		# print("Traffic Signals: ", traffic_signals)
		# print("Start Node: ", start_node)
		# print("End Node: ", end_node)
		# print("Horizontal Roads under Construction: ", horizontal_roads_under_construction)
		# print("Vertical Roads under Construction: ", vertical_roads_under_construction)
		# print("\n\n")

	except Exception as e:
		print('Your task_1a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	try:

		## Connect to CoppeliaSim arena
		coppelia_client = RemoteAPIClient()
		sim = coppelia_client.getObject('sim')

		## Define all models
		all_models = []

		## Setting up coppeliasim scene
		print("[1] Setting up the scene in CoppeliaSim")
		all_models = pb_theme.place_packages(medicine_package_details, sim, all_models)
		all_models = pb_theme.place_traffic_signals(traffic_signals, sim, all_models)
		all_models = pb_theme.place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_start_end_nodes(start_node, end_node, sim, all_models)
		print("[2] Completed setting up the scene in CoppeliaSim")
		print("[3] Checking arena configuration in CoppeliaSim")

	except Exception as e:
		print('Your task_4a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	pb_theme.send_message_via_socket(connection_1, "CHECK_ARENA")

	## Check if arena setup is ok or not
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		

		if message == "ARENA_SETUP_OK":
			print("[4] Arena was properly setup in CoppeliaSim")
			break
		elif message == "ARENA_SETUP_NOT_OK":
			print("[4] Arena was not properly setup in CoppeliaSim")
			connection_1.close()
			# connection_2.close()
			server.close()
			sys.exit()
		else:
			pass

	## Send Start Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_START")
	
	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STARTED_CORRECTLY":
			print("[5] Simulation was started in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STARTED_CORRECTLY":
			print("[5] Simulation was not started in CoppeliaSim")
			sys.exit()

	## Send Start Command to Raspberry Pi to start execution
	pb_theme.send_message_via_socket(connection_2, "START")

	#### pass config_image in this function task_4b_implementation(sim,config_image,start_node,end_node,traffic_signals,connection
	task_4b_implementation(sim,config_img,start_node,end_node,traffic_signals,connection_2)

	## Send Stop Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_STOP")

	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STOPPED_CORRECTLY":
			print("[6] Simulation was stopped in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STOPPED_CORRECTLY":
			print("[6] Simulation was not stopped in CoppeliaSim")
			sys.exit()
