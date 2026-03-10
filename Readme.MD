🎮 Subway Surfers — Gesture Controller
Control Subway Surfers (or any arrow-key game) using your body or hand — no keyboard needed. Two controller modes included.

🕹️ Two Controller Modes
FileModeUsesbody_controller.pyFull body poseShoulders, arms, leanhand_controller.pyOne hand onlyFingers, wrist position

📦 Requirements

Python 3.8+
Webcam

bashpip install opencv-python mediapipe pyautogui numpy

▶️ Run
bash# Body controller
python body_controller.py

# Hand controller
python hand_controller.py

Make sure Subway Surfers (or your browser/emulator) is the active window before gesturing.


🧍 Body Controller — Gestures
ActionGesture⬆️ JumpRaise both arms above shoulders⬇️ RollCross arms on chest⬅️ Left laneLean body left➡️ Right laneLean body right
Tips:

Stand ~1.5–2m from your webcam so your full upper body is visible
Press R to recalibrate if detection feels off
Keep your background simple for better pose detection


🖐️ Hand Controller — Gestures
ActionGesture⬆️ JumpOpen hand — 5 fingers⬇️ RollFist — 0 fingers⬅️ Left laneMove hand to left side of frame➡️ Right laneMove hand to right side of frame
Tips:

Keep your hand clearly visible and well-lit
The frame is divided into thirds: left (0–30%), center (30–70%), right (70–100%)

📄 License
MIT — free to use and modify.