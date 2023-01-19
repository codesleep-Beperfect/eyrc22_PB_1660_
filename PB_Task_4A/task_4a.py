'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
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
# Filename:			task_4a.py
# Functions:		[ Comma separated list of functions in this file ]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
map_str_int={
    'A':-0.8800,'B':-0.5300,'C':-0.1800,'D':0.1700,'E':0.5350,'F':0.8800,
    '1':+0.8800,'2':+0.5300,'3':+0.1800,'4':-0.1700,'5':-0.5350,'6':-0.8800
}
##############################################################

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
    # print(packages_models_directory)
    arena = sim.getObject('/Arena')    
####################### ADD YOUR CODE HERE #########################
    # print(medicine_package_details)
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

    # t=sim.loadModel(traffic_sig_model)
    # sim.setObjectPosition(t,arena,(0.8800,0.8800,0.1))
    # sim.setObjectParent(t,arena)
    # print(t)
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
    # print(horizontal_roads_under_construction)
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

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "/test_imgs/"

    i = 0
    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')
    # cv2.imshow('t',config_img)
    # print(img_dir)
    # cv2.waitKey(0)
    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed    
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters['medicine_packages']
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)

   
    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed    
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            