import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,   
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        return frame

    def get_landmarks(self, frame):
        landmarks = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = frame.shape

            for lm in hand.landmark:
                landmarks.append((int(lm.x * w), int(lm.y * h)))

            self.mp_draw.draw_landmarks(
                frame, hand, self.mp_hands.HAND_CONNECTIONS
            )
        return landmarks
