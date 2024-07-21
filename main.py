from model.MPLandmarks import MPHandLandmarks
from model.MouseGestures import MouseGestures
import cv2
import mediapipe as mp

import time

handLandmark = MPHandLandmarks()
mouseEvent = MouseGestures()
detector = handLandmark.handLandmarkerOptionns

cap = cv2.VideoCapture(cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 30)
 
while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        results = detector.detect_for_video(mp_image, timestamp_ms=int(time.time() * 1000))
        # print(img)

        annotated_image = mouseEvent.drawHandLandmarks(mp_image.numpy_view(), results)
        initialize_mouse = mouseEvent.setInitForMouseGestures()
        mouseMoves = mouseEvent.checkMouseEvent(annotated_image)
        # print(annotated_image);

        cv2.imshow("Image Capture", annotated_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


