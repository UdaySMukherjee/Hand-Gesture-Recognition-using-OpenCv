import cv2
import mediapipe
import numpy as np
import HandTrackingModule as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
cap.set(3 , 640)
cap.set(4 , 480)
# 3 and 4 are for setting the Width and height of the camera window respectively

detector = ht.HandDetector()
# Object for the HandTrackingModule we created


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Above things are all initialisation

# volume.GetMute()
# We do not need this statement

volRange = volume.GetVolumeRange()
'''We see that the minimum range is -65 and the maximum is 0'''
# volume.SetMasterVolumeLevel(-20.0, None)
# When it is set to -20 then our volume is 26 and when it is 0 then it actually our volume is 100

'''volume.GetVolumeRange() will give the value in the form of a tuple with the minimum value , maximum value and another parameter'''
minVol = volRange[0]
maxVol = volRange[1]




while(True):
    _ , img = cap.read()
    img = cv2.flip(img , 1)
    # Lateral shift

    img = detector.findHands(img)
    # Sending to the method created in the HandTrackingModule

    idList = detector.findPosition(img , False)
    if(len(idList)!=0):
        x1 , y1 = idList[4][1] , idList[4][2]
        # Finding the x and y coordinate for the index fingure

        x2 , y2 = idList[8][1] , idList[8][2]
        # Same as the above but this is for the thumb

        x3 , y3 = (x1 + x2)//2 , (y1 + y2)//2
        cv2.circle(img , (x1 , y1) , 15 , (255  , 0 , 255) , cv2.FILLED)
        cv2.circle(img , (x2 , y2) , 15 , (255  , 0 , 255) , cv2.FILLED)
    
        cv2.line(img , (x1 , y1) , (x2 , y2) , (255 , 0 , 255) , 3)

        cv2.circle(img , (x3 , y3) , 15 , (255 , 0 , 255) , cv2.FILLED)

        # Now we will calculate the length on the basis of which the volume will be generated
        length = math.hypot(x2 - x1 , y2 - y1)
        # hypot will give the length of the hypotenuse line
        
        print(length)
        #  Now hereafter for the volume functions we have to take in a library 
        '''Here we see the maximum length coming to be almost 400 and the minimum length to be 15'''
        if length<=50:
            cv2.circle(img , (x3 , y3) , 15 , (0 , 255 , 0) , cv2.FILLED)
            # This will turn the middle point to be a kind of button when the 
        

        '''Converting length to volume range'''
        # Volume range is from -65 to 0

        vol = np.interp(length , [50 , 400] , [minVol , maxVol])
        # This method will change it proportionately
        # [50 , 400] are the minimum and the maximum lengths of the line
        # Corresponding to which the min and the max volumes are given in the list beside

        print(int(length) , vol)
        volume.SetMasterVolumeLevel(vol , None)
         
        volBar = np.interp(length , [50 , 400] , [400 , 150])
        # Here 400 is minimum because the coordinates are inverted here and origin is in the top left corner of the screen
  
        cv2.rectangle(img , (50 , 150) , (85 , 400) , (0 , 255 , 0) , 3)
        # 3 is the synonym for not filling but just the thickness of the outline
        cv2.rectangle(img , (50 , int(volBar)) , (85 , 400) , (0 , 255 , 0) , cv2.FILLED)
        
        volPercent = np.interp(length , [50 , 400] , [0 , 100])
        cv2.putText(img , f'{int(volPercent)} %' , (40 , 100) , cv2.FONT_HERSHEY_SCRIPT_COMPLEX , 1 , (255 , 0 , 0) , 3)
        
    cv2.imshow("Result" , img)
    cv2.waitKey(1)