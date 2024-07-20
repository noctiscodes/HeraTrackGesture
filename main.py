from model.MPLandmarks import MPHandLandmarks
import cv2
import time

handLandmark = MPHandLandmarks()

cap = cv2.VideoCapture(cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 30)

cTime = 0
pTime = 0

while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        flip_img = handLandmark.findHands(img)
        hand_lm_list, bbox = handLandmark.findPosition(flip_img)

        cTime = time.time()
        #store frame
        fps = 1 / (cTime - pTime)
        #swap previous time with current
        pTime = cTime

        #displays fps
        cv2.putText(flip_img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image Capture", flip_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()


