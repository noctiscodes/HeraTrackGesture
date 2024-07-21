import unittest

import cv2
import mediapipe as mp

class TestHandLandmark(unittest.TestCase):
    def setUp(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def test_findHands(self):
        img = cv2.imread('d:/Projects/HeraTrackGesture/tests/test_img.jpg')
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        self.assertTrue(results.multi_hand_landmarks)

if __name__ == '__main__':
    unittest.main()