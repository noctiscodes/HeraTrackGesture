from model.MPLandmarks import MPHandLandmarks
from model.MouseGestures import MouseGestures
import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

import time

handLandmark = MPHandLandmarks()
mouseEvent = MouseGestures()
detector = handLandmark.handLandmarkerOptionns

wdthCam, hthCam = 740, 480

cap = cv2.VideoCapture(cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 30)

# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    
while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        

        # results = landmarker.detect_for_video(mp_image, timestamp_ms=int(time.time() * 1000))

        results = detector.detect_for_video(mp_image, timestamp_ms=int(time.time() * 1000))
        # mouseEvent.click(mp_image, results.hand_landmarks)
        

        # print(img)

        # annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), results)
        # annotated_image = handLandmark.drawHandLandmarks(mp_image.numpy_view(), results)
        annotated_image = mouseEvent.drawHandLandmarks(mp_image.numpy_view(), results)
        initialize_mouse = mouseEvent.setInitForMouseGestures()
        # position = handLandmark.findPos(annotated_image, results)
        # checkFingers = handLandmark.fingersUp()
        mouseMoves = mouseEvent.checkMouseEvent(annotated_image)
        # print(annotated_image);

        cv2.imshow("Image Capture", annotated_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


