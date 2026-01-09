from collections import deque

class GestureRecognizer:
    def __init__(self):
        self.x_positions = deque(maxlen=5)  # store last 5 frames

    def detect_swipe(self, landmarks):
        if not landmarks:
            self.x_positions.clear()
            return None

        x = landmarks[8][0]  # index finger tip X
        self.x_positions.append(x)

        if len(self.x_positions) < 5:
            return None

        diff = self.x_positions[-1] - self.x_positions[0]

        if diff > 60:      # 🔥 faster response
            self.x_positions.clear()
            return "RIGHT"
        elif diff < -60:
            self.x_positions.clear()
            return "LEFT"

        return None

    def detect_fist(self, landmarks):
        if not landmarks:
            return False

        finger_tips = [8, 12, 16, 20]
        wrist_y = landmarks[0][1]

        folded = sum(landmarks[tip][1] > wrist_y for tip in finger_tips)
        return folded == 4
