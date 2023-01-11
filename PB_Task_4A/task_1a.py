'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
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
	# traffic_signals = []
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
			
	# 		if red == 255:
	# 			loc = chr(64+j)+str(i) 
	# 			traffic_signals.append(loc)
	# traffic_signals.sort()

	##################################################

	return start_node, end_node





##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############

	for i in range(1, 7):
		for j in range(1, 7):
			red = maze_image[i*100, j*100][2]
			if red == 255:
				loc = chr(64+j)+str(i) 
				traffic_signals.append(loc)
	
	##################################################
	traffic_signals.sort()
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
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
	t=2
    
	i=6
	while i>=1:
		t=2
		for j in range(1,6):
			mid_x=int((j*100+t*100)/2)
			test_img=maze_image[i*100,mid_x-10:mid_x+10]
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
	##############	ADD YOUR CODE HERE	##############
	
	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):
	vertical_roads_under_construction = []
	t=2
	j=1
	while j<7:
		t=2
		for i in range(1,6):
			mid_y=int((i*100+(t)*100)/2)
			test_img=maze_image[mid_y,j*100]
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
	



def detect_medicine_packages(maze_image):

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
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############
	gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)
	img_hsv=cv2.cvtColor(maze_image,cv2.COLOR_BGR2HSV)

	
	for i in range(1,7):
		cropped=gray[100:200,i*100:(i+1)*100]
		color_cr=maze_image[100:200,i*100:(i+1)*100]
		


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
			medicine_packages_present.append(local_list)

	medicine_packages_present.sort()
	##################################################

	return medicine_packages_present

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

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
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	trafic_signals=detect_traffic_signals(maze_image)
	arena_parameters['traffic_signals']=trafic_signals
	horizontal_roads=detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['horizontal_roads_under_construction']=horizontal_roads
	vertical_roads=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=vertical_roads
	medical_packages=detect_medicine_packages(maze_image)
	arena_parameters['medicine_packages']=medical_packages
	start,end=detect_all_nodes(maze_image)
	arena_parameters['start_node']=start
	arena_parameters['end_node']=end
	
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()