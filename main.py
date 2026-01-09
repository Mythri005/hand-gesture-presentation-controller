import cv2
import pyautogui
import time
import pygetwindow as gw

from hand_tracker import HandTracker
from gestures import GestureRecognizer

pyautogui.FAILSAFE = False

# -----------------------------
# Helper: Focus slideshow window
# -----------------------------
def focus_presentation():
    windows = gw.getAllTitles()
    for title in windows:
        if "WPS" in title or "PowerPoint" in title or "Presentation" in title:
            win = gw.getWindowsWithTitle(title)[0]
            win.activate()
            return True
    return False


print("\n📽️ HAND GESTURE PRESENTATION CONTROLLER\n")
print("👉 STEP 1: Open presentation (WPS / PowerPoint)")
print("👉 STEP 2: Start Slide Show (F5)")
input("👉 STEP 3: Press ENTER once slideshow is READY...")

print("\n🔎 Trying to focus slideshow window...")
time.sleep(1)

if focus_presentation():
    print("✅ Slideshow window focused")
else:
    print("⚠️ Could not auto-detect slideshow window")
    print("👉 Click once on the slideshow manually")

time.sleep(2)

# -----------------------------
# Initialize
# -----------------------------
cap = cv2.VideoCapture(0)
tracker = HandTracker()
gesture = GestureRecognizer()

last_action_time = 0
cooldown = 0.5

print("\n✅ Gesture Control Activated")
print("➡ Swipe Right  → Next Slide")
print("⬅ Swipe Left   → Previous Slide")
print("✊ Fist        → Pause / Resume")
print("❌ Press ESC to Exit\n")

# -----------------------------
# Main loop
# -----------------------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    tracker.find_hands(frame)
    landmarks = tracker.get_landmarks(frame)

    current_time = time.time()

    if landmarks and (current_time - last_action_time > cooldown):
        swipe = gesture.detect_swipe(landmarks)
        fist = gesture.detect_fist(landmarks)

        if swipe == "RIGHT":
            focus_presentation()
            pyautogui.press("right")
            print("➡ Next Slide")
            last_action_time = current_time

        elif swipe == "LEFT":
            focus_presentation()
            pyautogui.press("left")
            print("⬅ Previous Slide")
            last_action_time = current_time

        elif fist:
            focus_presentation()
            pyautogui.press("space")
            print("⏸ Pause / Resume")
            last_action_time = current_time

    cv2.imshow("Camera (Gesture Detection)", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("\n👋 Gesture controller stopped")
