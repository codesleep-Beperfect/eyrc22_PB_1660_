'''
*****************************************************************************************
*
*        		     ===============================================
*           		       Pharma Bot (PB) Theme (eYRC 2022-23)
*        		     ===============================================
*
*  This script contains all the past implemented functions of Pharma Bot (PB) Theme 
*  (eYRC 2022-23).
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			PB_theme_functions.py
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
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
import math
from cv2 import aruco
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
map_str_int={
    'A':-0.8800,'B':-0.5300,'C':-0.1800,'D':0.1700,'E':0.5350,'F':0.8800,
    '1':+0.8800,'2':+0.5300,'3':+0.1800,'4':-0.1700,'5':-0.5350,'6':-0.8800
}

##############################################################


################## ADD SOCKET COMMUNICATION ##################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 3D for setting up a Socket
Communication Server in this section
"""

def setup_server(host, port):

	"""
	Purpose:
	---
	This function creates a new socket server and then binds it 
	to a host and port specified by user.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`server` : [ socket object ]
	---

	
	Example call:
	---
	server = setupServer(host, port)
	""" 

	server = None

	##################	ADD YOUR CODE HERE	##################
	server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((host,port))
	server.listen(5)

	##########################################################

	return server

def setup_connection(server):
	"""
	Purpose:
	---
	This function listens for an incoming socket client and
	accepts the connection request

	Input Arguments:
	---
	`server` :	[ socket object ]
			socket object created by setupServer() function
	Returns:
	---
	`server` : [ socket object ]
	
	Example call:
	---
	connection = setupConnection(server)
	"""
	connection = None
	address = None

	##################	ADD YOUR CODE HERE	##################
	while connection==None and address==None:
		print("Trying to connect")
		connection,address=server.accept()

	##########################################################

	return connection, address

def receive_message_via_socket(connection):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################
	message=connection.recv(80)
	message=message.decode("utf-8")

	##########################################################

	return message

def send_message_via_socket(connection, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################
	connection.send(bytes(message,"utf-8"))

	##########################################################

##############################################################
##############################################################

######################### ADD TASK 2B ########################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 2B for reading QR code from
CoppeliaSim arena in this section
"""

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the CoppeliaSim vision sensor's 
	field of view and returns the message encoded into it.

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
	
	##############  ADD YOUR CODE HERE  ##############
	vision_sensor_handle=sim.getObjectHandle('/Diff_Drive_Bot/vision_sensor')
	img,shape=sim.getVisionSensorImg(vision_sensor_handle)
	img=np.frombuffer(img,dtype=np.uint8).reshape(shape[0],shape[1],3)
	img=cv2.flip(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),0)
	qrs=decode(img)
	for qr in qrs:
		qr_message= qr.data.decode('UTF-8')

	##################################################

	return qr_message

##############################################################
##############################################################

############### ADD ARENA PARAMETER DETECTION ################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 1A and 3A for detecting arena parameters
from configuration image in this section
"""

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

    ##############	ADD YOUR CODE HERE	##############
	for i in range(1, 7):
		for j in range(1, 7):
			red =image[i*100, j*100][2]
			if red == 255:
				loc = chr(64+j)+str(i) 
				traffic_signals.append(loc)

    ##################################################
	traffic_signals.sort()
	for i in range(1, 7):
		for j in range(1, 7):
			red = image[i*100, j*100][2]
			green=image[i*100,j*100][1]

			purple=image[i*100,j*100]

			if purple[0]==189 and purple[1]==43 and purple[2]==105:
				end_node=end_node+(chr(64+j)+str(i))
			if green==255:
				start_node=start_node+(chr(64+j)+str(i))
	return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(image):	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	t=2
    
	i=6
	while i>=1:
		t=2
		for j in range(1,6):
			mid_x=int((j*100+t*100)/2)
			test_img=image[i*100,mid_x-10:mid_x+10]
			if test_img.all():
				loc=chr(64+j)+str(i)
				loc1=chr(64+t)+str(i)
				loc2=loc+"-"+loc1
				horizontal_roads_under_construction.append(loc2)
			t=t+1
		i=i-1
	horizontal_roads_under_construction.sort()

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	t=2
	j=1
	while j<7:
		t=2
		for i in range(1,6):
			mid_y=int((i*100+(t)*100)/2)
			test_img=image[mid_y,j*100]
            # print(test_img)
			if test_img.all():
				loc=chr(64+j)+str(i)
				loc1=chr(64+j)+str(t)
				loc2=loc+"-"+loc1
				vertical_roads_under_construction.append(loc2)
                # print((j,i))
			t=t+1
		j=j+1
	
	##################################################
	
	return vertical_roads_under_construction

def detect_medicine_packages(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

	
	for i in range(1,7):
		cropped=gray[100:200,i*100:(i+1)*100]
		color_cr=image[100:200,i*100:(i+1)*100]
		


		_, threshold = cv2.threshold(cropped, 190, 255, cv2.THRESH_BINARY)

		contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		j=0
		for contour in contours:
			if j==0:
				j=j+1
				continue
			
			approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
		

			cv2.drawContours(cropped, [contour], 0, (0, 0, 255), 5)
		

			M = cv2.moments(contour)
			if M['m00'] != 0.0:
				x = int(M['m10']/M['m00'])
				y = int(M['m01']/M['m00'])

			
			j=j+1
			color=""
			shape=""
			shop_number="Shop_"+str(i)
			if(color_cr[y,x][0]==255 and color_cr[y,x][1]==255 and color_cr[y,x][2]==0):
				color=color+"Skyblue"
			elif(color_cr[y,x][0]==0 and color_cr[y,x][1]==127 and color_cr[y,x][2]==255):
				color=color+"Orange"
			elif(color_cr[y,x][0]==180 and color_cr[y,x][1]==0 and color_cr[y,x][2]==255):
				color=color+"Pink"
			else:
				color=color+"Green"

				

			if len(approx) == 3:
				shape=shape+"Triangle"


			elif len(approx) == 4:
				shape=shape+"Square"
	
			else:
				shape=shape+"Circle"
				
			
			local_list=[]
			local_list.append(shop_number)
			local_list.append(color)
			local_list.append(shape)
			local_list.append([100*i+x,y+100])
			medicine_packages.append(local_list)

	medicine_packages.sort()

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
	trafic_signals,start,end=detect_all_nodes(maze_image)
	arena_parameters['traffic_signals']=trafic_signals
	arena_parameters['start_node']=start
	arena_parameters['end_node']=end
	horizontal_roads=detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['horizontal_roads_under_construction']=horizontal_roads
	vertical_roads=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=vertical_roads
	medical_packages=detect_medicine_packages(maze_image)
	arena_parameters['medicine_packages']=medical_packages
	
	

    ##################################################

	return arena_parameters

##############################################################
##############################################################

####################### ADD ARENA SETUP ######################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 4A for setting up the CoppeliaSim
Arena according to the configuration image in this section
"""

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    

####################### ADD YOUR CODE HERE #########################
    for shop,color,shape,centroid in medicine_package_details:
        shop_no=int(shop[-1])
        # print(shop_no)
        x,y=centroid[0]-100*shop_no,centroid[1]-100
        packet=0
        if x==30 and y==30:
            packet=1
        if x==70 and y==30:
            packet=2
        if x==30 and y==70:
            packet=3
        if x==70 and y==70:
            packet=4
        packet=packet-1
        x_coor=-(0.8800-0.36*(shop_no-1)-0.04*(2*packet+1)-0.01+0.005)
        # print(packet)
        y_coor=+(0.6650)
        shape_3d=''
        if shape=='Square':
            shape_3d='_cube'
        if shape =='Triangle':
            shape_3d='_cone'
        if shape=='Circle':
            shape_3d='_cylinder'
        
        path_file=color+shape_3d+".ttm"
        temp_path=os.path.join(packages_models_directory,path_file)
        # print(temp_path)
        # print(temp_path)
        t=sim.loadModel(temp_path)
        sim.setObjectParent(t,arena)
        sim.setObjectAlias(t,color+shape_3d)
        sim.setObjectPosition(t,arena,(x_coor,y_coor,0.003))
        all_models.append(t)


####################################################################

    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    print(traffic_signals)
    for node in traffic_signals:
        t=sim.loadModel(traffic_sig_model)
        # print(t)

        sim.setObjectParent(t,arena)
        sim.setObjectAlias(t,"Signal_"+node)
        # node_list=list(node)
        x=map_str_int[node[0]]
        y=map_str_int[node[1]]
        sim.setObjectPosition(t,arena,(x,y,0.15588))
        all_models.append(t)

####################################################################

    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   

####################### ADD YOUR CODE HERE #########################
    t=sim.loadModel(start_node_model)
    # print(t)
    sim.setObjectParent(t,arena)
    sim.setObjectAlias(t,"Start_Node")
        # node_list=list(node)
    x=map_str_int[start_node[0]]
    y=map_str_int[start_node[1]]
    sim.setObjectPosition(t,arena,(x,y,0.15588))
    all_models.append(t)
    t=sim.loadModel(end_node_model)
    # print(t)
    sim.setObjectParent(t,arena)
    sim.setObjectAlias(t,"End_Node")
        # node_list=list(node)
    x=map_str_int[end_node[0]]
    y=map_str_int[end_node[1]]
    sim.setObjectPosition(t,arena,(x,y,0.15588))
    all_models.append(t)

####################################################################

    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  

####################### ADD YOUR CODE HERE #########################
    for roads in horizontal_roads_under_construction:
        t=sim.loadModel(horiz_barricade_model)
        sim.setObjectParent(t,arena)
        sim.setObjectAlias(t,"Horizontal_missing_road_"+roads[0]+roads[1]+"_"+roads[3]+roads[4])
        x1,y1=map_str_int[roads[0]],map_str_int[roads[1]]
        x2,y2=map_str_int[roads[3]],map_str_int[roads[4]]
        x3=(x1+x2)/2
        y3=(y1+y2)/2
        sim.setObjectPosition(t,arena,(x3,y3,0.003))
        all_models.append(t)

####################################################################

    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    for roads in vertical_roads_under_construction:
        t=sim.loadModel(vert_barricade_model)
        sim.setObjectParent(t,arena)
        sim.setObjectAlias(t,"Vertical_missing_road_"+roads[0]+roads[1]+"_"+roads[3]+roads[4])
        x1,y1=map_str_int[roads[0]],map_str_int[roads[1]]
        x2,y2=map_str_int[roads[3]],map_str_int[roads[4]]
        x3=(x1+x2)/2
        y3=(y1+y2)/2
        sim.setObjectPosition(t,arena,(x3,y3,0.003))
        all_models.append(t)

####################################################################

    return all_models

##############################################################
def detect_ArUco_details(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary such
    that the id of the ArUco marker is the key and a list of details of the marker
    is the value for each item in the dictionary. The list of details include the following
    parameters as the items in the given order
        [center co-ordinates, angle from the vertical, list of corner co-ordinates] 
    This order should be strictly maintained in the output

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `ArUco_details_dict` : { dictionary }
            dictionary containing the details regarding the ArUco marker
    
    Example call:
    ---
    ArUco_details_dict = detect_ArUco_details(image)
    """    

    ##############	ADD YOUR CODE HERE	##############
    ArUco_details_dict = {} 
    ArUco_corners = {}
    ARUCO_DICT = {
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    for (arucoName, arucoDict) in ARUCO_DICT.items():
        arucoDict = cv2.aruco.Dictionary_get(arucoDict)
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)
        # if at least one ArUco marker was detected display the ArUco
        # name to our terminal
        
        if len(corners) > 0:
            i=0

            for id in ids:
                
                ArUco_corners[id[0]]=corners[i][0]
                i=i+1
            
             
    
    for (id,points) in ArUco_corners.items():
        # print(points)
        point_1=points[0]
        point_2=points[1]
        point_3=points[2]
        aruco_mid_x=round((point_1[0]+point_3[0])/2)
        aruco_mid_y=round((point_1[1]+point_3[1])/2)

        mid_x_1_2=(point_1[0]+point_2[0])/2
        mid_y_1_2=(point_1[1]+point_2[1])/2
        
        shifted_x=mid_x_1_2-aruco_mid_x
        shifted_y=-mid_y_1_2+aruco_mid_y
        # print(-int(math.atan2(shifted_x,shifted_y)*57.29))
        ArUco_details_dict[int(id)]=[[aruco_mid_x,aruco_mid_y],-round(math.atan2(shifted_x,shifted_y)*180/3.141592653589793)]
    ##################################################
    
    return ArUco_details_dict, ArUco_corners 

##############################################################

def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	for i in range(1,7):
		for j in range(1,7):
			point={}
				#i+1,j
				#i-1,j
				#i,j+1
				#i,j-1
			
			if i>=1 and i<=6 and j+1>=1 and j+1<=6:
				mid_x=int(((j+1)*100+j*100)/2)
				test_img=image[i*100,mid_x-10:mid_x+10]
				if test_img.all()==0:
					point[""+(chr(64+j+1)+str(i))]=1
				
			if i>=1 and i<=6 and j-1>=1 and j-1<=6:
				mid_x=int(((j-1)*100+j*100)/2)
				test_img=image[i*100,mid_x-10:mid_x+10]
				if test_img.all()==0:
					point[""+(chr(64+j-1)+str(i))]=1

			if i+1>=1 and i+1<=6 and j>=1 and j<=6:
				mid_y=int(((i+1)*100+i*100)/2)
				test_img=image[mid_y,j*100]
				if test_img.all()==0:
					point[""+(chr(64+j)+str(i+1))]=1
			if i-1>=1 and i-1<=6 and j>=1 and j<=6:
				mid_y=int(((i-1)*100+i*100)/2)
				test_img=image[mid_y,j*100]
				if test_img.all()==0:
					point[""+(chr(64+j)+str(i-1))]=1
				
			# sorted(point)
			point_sorted={}
			for t in sorted(point):
				point_sorted[t]=point[t]
				

			paths[""+(chr(64+j)+str(i))]=point_sorted
        

	##################################################
	paths_sorted={}
	for i in sorted(paths):
		paths_sorted[i]=paths[i]
	# print(paths_sorted)
	return paths_sorted
def find_minimum(node,vis,dist):
    min_dis=100000000
    curr_nod=""
    # print(vis)
    for i in vis:
        # print(i)
        if(vis[i]==0):
			# #### change here
           if dist[i]<min_dis:
            min_dis=dist[i]
            # curr_node=""
            curr_nod=i
    return curr_nod

def path_planning(graph, start, end):
	# print(graph)
	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	node=36
	dist={}
	for i in graph:
		dist[i]=1e9
	vis={}
	path={}
	for i in graph:
		vis[i]=0
		path[i]=""
		dist[start]=0
	for i in range(node):
		# find  minimum  node
		min_node=find_minimum(node,vis,dist)
		# print(min_node)
		vis[min_node]=1
		if min_node=="":
			continue 
		for j in graph[min_node]:
			# print(graph[min_node][j])
			# print(j)
			if(graph[min_node][j]+dist[min_node]<dist[j]):
				dist[j]=graph[min_node][j]+dist[min_node]
				path[j]=min_node
	curr_node=end
	backtrace_path=[]
	while True:
		if curr_node==start:
			break
		backtrace_path.append(curr_node)
		curr_node=path[curr_node]

	backtrace_path.append(start)
	backtrace_path.reverse()
	##################################################

	# print(backtrace_path)
	return backtrace_path
robot_direction="NORTH"
def paths_to_moves(paths, traffic_signal):
	global robot_direction
	# print(traffic_signal)																					
	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	
	for i in range(len(paths)-1):
		node_curr=paths[i]
		node_next=paths[i+1]
		if node_curr in traffic_signal:
			list_moves.append("WAIT_5")
		# print(node_curr[0])
		if node_curr[0]==node_next[0]:
			if node_next[1]<node_curr[1]:
				if robot_direction=="NORTH":
					list_moves.append("STRAIGHT")
					robot_direction="NORTH"
				elif robot_direction=="WEST":
					list_moves.append("RIGHT")
					robot_direction="NORTH"
				elif robot_direction=="EAST":
					list_moves.append("LEFT")
					robot_direction="NORTH"
					
				elif robot_direction=="SOUTH":
					print("Line no.1136")
					list_moves.append("REVERSE")
					robot_direction="NORTH"
			elif node_next[1]>node_curr[1]:
				if robot_direction=="NORTH":
					print("Line no.1141")
					list_moves.append("REVERSE")
					robot_direction="SOUTH"
					
				elif robot_direction=="WEST":
					list_moves.append("LEFT")
					robot_direction="SOUTH"
				elif robot_direction=="EAST":
					list_moves.append("RIGHT")
					robot_direction="SOUTH"
				elif robot_direction=="SOUTH":
					list_moves.append("STRAIGHT")
					robot_direction="SOUTH"
		else:
			if node_next[0]<node_curr[0]:
				if robot_direction=="NORTH":
					list_moves.append("LEFT")
					robot_direction="WEST"
				elif robot_direction=="WEST":
					list_moves.append("STRAIGHT")
					robot_direction="WEST"
				elif robot_direction=="EAST":
					print("Line no.1163")
					list_moves.append("REVERSE")
					robot_direction="WEST"
				elif robot_direction=="SOUTH":
					list_moves.append("RIGHT")
					robot_direction="WEST"
			else :
				if robot_direction=="NORTH":
					list_moves.append("RIGHT")
					robot_direction="EAST"
				elif robot_direction=="WEST":
					print("Line no.1174")
					list_moves.append("REVERSE")
					robot_direction="EAST"
				elif robot_direction=="EAST":
					list_moves.append("STRAIGHT")
					robot_direction="EAST"
				elif robot_direction=="SOUTH":
					list_moves.append("LEFT")
					robot_direction="EAST"

	##################################################

	return list_moves
