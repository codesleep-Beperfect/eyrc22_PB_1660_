'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

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
			red = image[i*100, j*100][2]
			green=image[i*100,j*100][1]

			purple=image[i*100,j*100]

			if purple[0]==189 and purple[1]==43 and purple[2]==105:
				end_node=end_node+(chr(64+j)+str(i))
			if green==255:
				start_node=start_node+(chr(64+j)+str(i))
			
			if red == 255:
				loc = chr(64+j)+str(i) 
				traffic_signals.append(loc)
	traffic_signals.sort()

	##################################################

	return traffic_signals, start_node, end_node


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
	t_s,s_node,e_node=detect_all_nodes(maze_image)
	arena_parameters["traffic_signals"]=t_s
	arena_parameters["start_node"]=s_node
	arena_parameters["end_node"]=e_node
	arena_parameters["paths"]=detect_paths_to_graph(maze_image)

	##################################################
	# print(arena_parameters)
	return arena_parameters

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

def paths_to_moves(paths, traffic_signal):
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
	robot_direction="NORTH"
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
					list_moves.append("REVERSE")
					robot_direction="NORTH"
			elif node_next[1]>node_curr[1]:
				if robot_direction=="NORTH":
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

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)

			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
