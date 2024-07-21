import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2

# model\hand_landmarker.task
class MPHandLandmarks:
    def __init__(self, model='model/hand_landmarker.task', num_hands=2, running_mode=mp.tasks.vision.RunningMode.VIDEO):
        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model),
            num_hands=num_hands,
            running_mode=running_mode)
        self.handLandmarker = vision.HandLandmarker
        self.handLandmarkerOptionns = self.handLandmarker.create_from_options(self.options)

        self.margin = 10
        self.font_size = 1
        self.font_thickness = 1
        self.handedness_text_color = (88, 205, 54)
        self.tipIds = [4, 8, 12, 16, 20]
        self.handPosList = []
        self.posList = []

        

    # Modified from mediapipe guide examples 
    def drawHandLandmarks(self, img, results):
        hand_landmarks_list = results.hand_landmarks
        handedness_list = results.handedness
        annoted_image = np.copy(img)
        bbox_list = []
        self.handPosList = []

        # print(results)

        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            # Draw the hand landmarks
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                for landmark in hand_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                annoted_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_utils.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=4),
                solutions.drawing_utils.DrawingSpec(color=(160, 199, 120), thickness=2, circle_radius=2),
            )

            # Get the location and size of the detected hand's bounding box.
            height, width, _ = annoted_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]

            self.handPosList.extend([ 
                [int(x_coordinates[idx] * width), int(y_coordinates[idx] * height), idx]
                for idx, landmark in enumerate(hand_landmarks)
            ])

            xmin1, xmax1 = int(min(x_coordinates) * width), int(max(x_coordinates) * width)
            ymin1, ymax1 = int(min(y_coordinates) * height), int(max(y_coordinates) * height)
            bbox_list.append([xmin1, ymin1, xmax1, ymax1])

            for idx in range(len(self.handPosList)):
                # Draws point number on hands
                cv2.putText(annoted_image, str(self.handPosList[idx][2]), (self.handPosList[idx][0] + 2, self.handPosList[idx][1] - 15), cv2.FONT_HERSHEY_PLAIN, self.font_size, self.handedness_text_color, self.font_thickness)
                # if idx in self.tipIds:
                #     cv2.circle(annoted_image, (self.handPosList[idx][0] + 5, self.handPosList[idx][1] - 50), 15, (255, 0, 255), cv2.FILLED)
            # Draws hand bounding box.
            cv2.rectangle(annoted_image, (xmin1 - 20, ymin1 - 20), (xmax1 + 20, ymax1 + 20), (0, 255, 0), 2)

        
            self.posList = self.handPosList

        return annoted_image
    
    def fingersUp(self):
        fingers = []

        if self.posList != []:
            if self.posList[0][0] > self.posList[self.tipIds[0] - 1][0]:
                fingers.append(0)
            else:
                fingers.append(1)

            for id in range(1, 5):
                if self.posList[self.tipIds[id]][1] < self.posList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                    
        # print(fingers)

        return fingers
    
    # def checkMouseEvent(self, img):
    #     pass
    