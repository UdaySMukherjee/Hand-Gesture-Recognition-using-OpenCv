import cv2
import mediapipe as mp
import time

'''https://mediapipe.readthedocs.io/en/latest/solutions/hands.html'''

class HandDetector():
    def _init_(self, mode = False , maxHands = 2 ,modelComplexity = 1,  detection_confidence = 0.5 , tracking_confidence = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.modelComplexity = modelComplexity
        self.mpHands = mp.solutions.hands
        # This initiates the pipelines 

        hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplexity ,self.detection_confidence ,self.tracking_confidence)
        # hands is the object
        #  Hands is the function
        self.hands = hands
        self.mpDraw = mp.solutions.drawing_utils
        #  This is the function for drawing
        # mpDraw is another object of the solutions.drawing_utils class
        
    def findHands(self , img , draw = True):
        # Here we will be drawing that's why we kept it true
        imageRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB )
        self.results = self.hands.process(imageRGB)
        # We are storing the variable result as an object variable so that we can access them outside this method
        # This method generates the landmarks
        # process is a method
    
        if(self.results.multi_hand_landmarks):  # This method checks whether the number of hands are more than 0
           for handlms in self.results.multi_hand_landmarks : 
               # hndlms are the individual hands among the multiple hands
                if draw:
                   self.mpDraw.draw_landmarks(img , handlms , self.mpHands.HAND_CONNECTIONS)
            # landmarks are the 21 2D points described to plot the hand
            # Here if we do draw_landmarks(img , mpHands) then only the dots or the landmarks will be printed
            
        return img
    


    def findPosition(self , img , draw ):
        # The draw is kept true because we may or may not draw in the image
        idList = []
        if(self.results.multi_hand_landmarks):  # This method checks whether the number of hands are more than 0
          Hand1 = self.results.multi_hand_landmarks[0]
          # We are considering that only one hand will come in the frame each time

          for id , lm in enumerate(Hand1.landmark):
                   # handlms are the individual hand and landmark are the array or the three values of that hand
                   # handlms.landmark gives the data of each and every landmark
                   # The values i.e x , y and z coordinates present in the lm are actually the screen ratio so we multiply it by the height and width to get the pixel value
                   h , w , c = img.shape
                   cx , cy = int(lm.x * w) , int(lm.y * h)
                   # Converting them to int as pixel value cannot be decimal
                #    print(id , cx , cy)
                   # This will give the x and y coordinates of the pixel
                   idList.append([id , cx , cy])
                #    We are putting an array or a list inside this list 
                # So that by giving each sub array's first element we can get the whole sub array


                   #  Now we will just decorate the fingertips a bit
                #    if (id == 4 or id == 8 or id == 12 or id == 16 or id == 20):
                #       cv2.circle(img , (cx , cy) , 15 , (255 , 0 , 255) , cv2.FILLED)
                #       # cx and cy are the coordinates of the centre of the landmarks

                   if draw:
                       cv2.circle(img , (cx , cy) , 15 , (255 , 0 , 255) ,cv2.FILLED)
        return idList

def main():
    cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
    # img = cv2.flip(img , 1)
    
    detector = HandDetector()
    
    # cap = cv2.VideoCapture(0 , cv2.CAP_DSHOW)
    # img = cv2.flip(img , 1)
    cTime = 0
    pTime = 0
    # For calculating the frames per second which the camera can identify
    
    while True:
       succes, img = cap.read()
       img = detector.findHands(img)
       cTime = time.time()  # This will give the current time
       fps  = 1/(cTime - pTime)
       # As here in the loop only a single frame comes by cap.read thus we write 1 divided by the change in time
       # Thus giving the frames per second value very accuartely
       pTime = cTime
       
       # previous Time (pTime)  value get replaced by the value of current Time(cTime) thus for the advancement in calculation
    
       cv2.putText(img , f'FPS : {int(fps)}' , (10,70) , cv2.FONT_HERSHEY_PLAIN , 3 , (0 , 0 , 0) , 3)
       # (10,70) is the coordinate or the pixel at which this text must be displayed
       # The value 3 represents the thickness and the length of the text
       
       idList = detector.findPosition(img , True)
       if(len(idList) != 0):
           print(idList)

       cv2.imshow("Image", img)
       cv2.waitKey(1)    


if __name__ == '_main_':
    main()