'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy 
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################


#####################################################################################
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
    Aruco_details,Aruco_corners=task_1b.detect_ArUco_details(image) 
#################################  ADD YOUR CODE HERE  ###############################
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

######################################################################################

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
#################################  ADD YOUR CODE HERE  ###############################
    Aruco_details1,Aruco_corners1=task_1b.detect_ArUco_details(image)
    # task_1b.mark_ArUco_image(frame,Aruco_details1, Aruco_corners1)
    # cv2.imshow('marked',frame)
    # print(Aruco_details)
    if Aruco_details1.get(5):
        x_pixel=Aruco_details1[5][0][0]
        y_pixel=Aruco_details1[5][0][1]
        # print(x_pixel,y_pixel)
        y_cop=0.0044*y_pixel-0.9787+0.03
        pixel_per_cm=103.85*y_cop*y_cop*y_cop*y_cop*y_cop-5.0625*y_cop*y_cop*y_cop*y_cop-81.685*y_cop*y_cop*y_cop-4.182*y_cop*y_cop+9.8966*y_cop+210.86
        x_cop=(215-x_pixel)*1.0/pixel_per_cm-0.1 
        # print(x_cop,y_cop)
######################################################################################
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
#################################  ADD YOUR CODE HERE  ###############################
    if len(scene_parameters):
        sim.setObjectPosition(aruco_handle,aruco_handle_3,[scene_parameters[0],scene_parameters[1],0])
        # if( scene_parameters[2]<=90):
        #     alpha=(90-scene_parameters[2])*0.0175
        # else :
        #     alpha=(scene_parameters[2]-90)*0.0175
        # print(scene_parameters[2])
        angle_rad=scene_parameters[2]*0.0175
        sim.setObjectOrientation(aruco_handle,sim.handle_world,[0,0,angle_rad])
######################################################################################

    return None

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################

    cap = cv2.VideoCapture(0)
    
    # cap2 = cv2.VideoCapture(0)
    while True:

        ret, frame = cap.read()
        frame=frame[40:,100:510]
        # print(frame.shape)
        # frame=cv2.resize(frame,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
        cameraMatrix=numpy.array([[669.2721006 ,   0.    ,     308.27537125],
 [  0.      ,   664.83129387 ,268.35372325],
 [  0.,           0.  ,         1.  ,      ]])
        dist=numpy.array([[-7.77722198e-01 , 2.17364635e-02, -7.01392560e-04 , 5.27929722e-03,
   1.30080094e+00]])
        h,  w = frame.shape[:2]
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# # Undistort 
        dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
        # Aruco_details,Aruco_corners=task_1b.detect_ArUco_details(frame)
        t=perspective_transform(dst)
        if len(t):
            # pass
            # t = cv2.undistort(t, cameraMatrix, dist, None, newCameraMatrix)
            a=transform_values(t)
            # print(a)
            set_values(a)
            # cv2.imshow('frame2',t)
            
        cv2.imshow('Frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#######################################################################################



    
