from model.MPLandmarks import MPHandLandmarks
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import pyautogui
import numpy as np
import cv2

class MouseGestures(MPHandLandmarks):

    def __init__(self):
        super().__init__()
        self.wCam, self.hCam = 640, 480
        self.wScr, self.hScr = pyautogui.size()
        self.plocCX, self.plocCY = 0, 0
        self.mouseX, self.mouseY = 0, 0
        self.smooteness = 3
        self.matchWindow = 200

        self.fingers = [0, 0, 0, 0, 0]
        self.thumb_tip = 0
        self.index_tip = 0
        self.middle_tip = 0
        self.ring_tip = 0
        self.pinky_tip = 0

    def setInitForMouseGestures(self):
        if self.posList != [] and len(self.fingersUp()) > 4:
            self.fingers = self.fingersUp()

        if len(self.fingers) > 4:
            # print(self.fingers)
            self.thumb_tip = self.fingers[0]
            self.index_tip = self.fingers[1]
            self.middle_tip = self.fingers[2]
            self.ring_tip = self.fingers[3]
            self.pinky_tip = self.fingers[4]

    def checkMouseEvent(self, img):
        if(self.posList != [] and len(self.fingersUp()) > 4):
            self.move(img, self.posList)
            self.left_click(img)
            self.right_click(img)


    def move(self, img, lmList):      
        self.mouseX, self.mouseY = lmList[8][:2]
        x, y = lmList[3][:2]
        if self.index_tip == 1 and self.middle_tip == 0:
            x = np.interp(self.mouseX, (self.matchWindow, self.wCam - self.matchWindow), (0, self.wScr))
            y = np.interp(self.mouseY, (self.matchWindow, self.hCam - self.matchWindow), (0, self.hScr))

            smoothX = (self.plocCX + (x - self.plocCX) / self.smooteness) - 3
            smoothY = (self.plocCY + (y - self.plocCY) / self.smooteness) - 5

            print(int(smoothX), int(smoothY))
            pyautogui.moveTo(smoothX, smoothY)
            cv2.circle(img, (int(self.mouseX), int(self.mouseY)), 15, (100, 57, 1), cv2.FILLED)

            self.plocCX, self.plocCY = smoothX, smoothY


    def left_click(self, img):

        if self.index_tip == 0 and self.middle_tip == 1:
            length, img, lineInfo = self.findDistance(8, 6, img)

            if length < 35:
                pyautogui.click(button='left')

    def right_click(self, img):
        if self.index_tip == 0 and self.middle_tip == 0:
            length, img, lineInfo = self.findDistance(12, 10, img)

            if length < 32:
                pyautogui.click(button='right')


    def doubleClick(self, img, lmList):
        pass

    def scroll(self, img, lmList):
        pass

    def drag(self, img, lmList):
        pass

    def rightClick(self, img, lmList):
        pass

    def leftClick(self, img, lmList):
        pass


    
