import mediapipe as mp
import cv2

class GameGestures():
    def __init__(self, modelComplexity=1, minDetectionConfidence=0.5, minTrackingConfidence=0.5):
        self.mpHolistic = mp.solutions.holistic
        self.initHolistic = self.mpHolistic.Holistic(min_detection_confidence=minDetectionConfidence, min_tracking_confidence=minTrackingConfidence)
        self.modelComplexity = modelComplexity
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence

    def processImage(self, img, model):
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = model.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img, results
        
    def drawLandmarks(self, img, results):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

   
        mp_drawing.draw_landmarks(
            img,
            results.left_hand_landmarks,
            self.mpHolistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=2))
        
        mp_drawing.draw_landmarks(
            img,
            results.right_hand_landmarks,
            self.mpHolistic.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=2))
        
        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            self.mpHolistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        

    def trainPose(self, img, lmList):
        pass
        
        
            


    # Game Mouse Gestures, for VR game purposes
    def gameMode(self, img, lmList):
        #switches to game mode
        pass

    def block(self, img, lmList):
        pass

    def taunt(self, img, lmList):
        pass

    def getOverHere(self, img, lmList):
        pass

    def jab(self, img, lmList):
        pass

    def punch(self, img, lmList):
        pass



def main():
    gameClass = GameGestures()
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        fps = cap.get(cv2.CAP_PROP_FPS)
        h, w = img.shape[:2]

        img, results = gameClass.processImage(img, gameClass.initHolistic)
        leftHand = results.left_hand_landmarks
        print(leftHand)
        gameClass.drawLandmarks(img, results)

        cv2.imshow("Image Capture", cv2.flip(img, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()