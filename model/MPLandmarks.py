import mediapipe as mp
import cv2

class MPHandLandmarks:
    def __init__(self, maxHands=2, mode=False, modelComplexity=1, trackerCon=0.5, detectionCon=0.5):
        self.maxHands = maxHands
        self.mode = mode
        self.trackerCon = trackerCon
        self.detectionCon = detectionCon
        self.modelComplexity = modelComplexity

        self.mpDraw = mp.solutions.drawing_utils
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.trackerCon, self.detectionCon)
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        # converting the image to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # processing the image
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        #array to store x and y coordinates
        xList =[]
        yList =[]

        #array to store bounding box are for the hand
        bbox=[]

        #array to store hand position coordinates according to screen
        self.handPosList = []
        #if hands are detected
        if self.results.multi_hand_landmarks:
            #store landmarks information according to number of hands detected
            myHand = self.results.multi_hand_landmarks[handNo]
            #for each joint in hand assign an id and return landmarks
            for id, lm in enumerate(myHand.landmark):
                #store height, width and of frame size
                h, w, c = img.shape
                #store coordinates of landmark point converted to pixel format
                cx, cy = int(lm.x * w), int(lm.y * h)
                #append x landmark coordinates
                xList.append(cx)
                #append y landmark coordinates
                yList.append(cy)
                #append landmark id coordinates, to determine the position of the hand to assign landmarks to
                self.handPosList.append([id, cx, cy])

                #customises hand joint points to a teal colour, this can be changed according
                #to user preferences
                if draw:
                    cv2.circle(img, (cx, cy), 10, (160, 199, 120), cv2.FILLED)

            #retrives hand position and retrives
            #the x and y coordinates, according min and max to
            #draw a bounding box
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            #this draws the bounding box, color: Green
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)  
            

        return self.handPosList, bbox
    
    def colorHands(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (160, 199, 120), cv2.FILLED)
        return lmList
    