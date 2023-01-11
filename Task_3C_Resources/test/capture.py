import cv2
import numpy as np
import cv2 
import numpy 
from  numpy import interp
# from zmqRemoteApi import RemoteAPIClient
import zmq

cap=cv2.VideoCapture(0)
counter=0
while True:
    ret, frame=cap.read()
    cv2.imshow('frame',frame)
    # string ="frame"

    if cv2.waitKey(1)&0xFF==ord('c'):
        name="frame"+str(counter)+".png"
        cv2.imwrite(name,frame)
        counter=counter+1
    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()