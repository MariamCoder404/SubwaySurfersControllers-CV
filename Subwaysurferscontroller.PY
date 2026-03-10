import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# Disable PyAutoGUI's safety feature
pyautogui.FAILSAFE = False


class SubwaySurfersController:
    """
    Main controller class that handles all gesture detection and game control.
    """
    
    def __init__(self):
        """
        Initialize the controller - sets up all the AI models and settings.
        """
        # Initialize MediaPipe Pose Detection
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=1
        )
        
        # For drawing skeleton on screen
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Different cooldowns for different actions
        self.last_action_time = {
            'jump': 0,
            'roll': 0,
            'left': 0,
            'right': 0
        }
        
        # Separate cooldowns - left/right need longer cooldown to prevent spam
        self.action_cooldowns = {
            'jump': 0.4,     # Can jump every 0.4 seconds
            'roll': 0.5,     # Can roll every 0.5 seconds
            'left': 0.9,     # IMPORTANT: Longer cooldown prevents wall collision
            'right': 0.9     # IMPORTANT: Longer cooldown prevents wall collision
        }
        
        # Calibration - learns your neutral standing position
        self.neutral_shoulder_x = None
        self.neutral_wrist_distance = None  # NEW: For detecting arms crossed
        self.calibrated = False
        
        # Gesture detection thresholds
        self.jump_threshold = 0.12
        self.lean_threshold = 0.10
        
    def calibrate(self, landmarks):
        """
        Learn the user's neutral standing position.
        """
        # Get key body positions
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        
        # Calculate neutral positions
        self.neutral_shoulder_x = (left_shoulder.x + right_shoulder.x) / 2
        
        # Calculate distance between wrists in neutral position
        self.neutral_wrist_distance = abs(left_wrist.x - right_wrist.x)
        
        self.calibrated = True
        print("✅ Calibrated! Stand with arms at sides.")
        print("💡 TIP: To ROLL, CROSS YOUR ARMS on your chest!")
        
    def detect_gesture(self, landmarks):
        """
        Gesture detection with CROSS ARMS for roll.
        """
        # If not calibrated yet, do calibration first
        if not self.calibrated:
            self.calibrate(landmarks)
            return None
        
        # Get all the body parts we need to track
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        
        # Calculate current positions
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        
        # Current distance between wrists
        current_wrist_distance = abs(left_wrist.x - right_wrist.x)
        
        # PRIORITY 1: JUMP - Both arms raised above shoulders
        if (left_wrist.y < left_shoulder.y - self.jump_threshold and 
            right_wrist.y < right_shoulder.y - self.jump_threshold):
            return 'jump'
        
        # PRIORITY 2: ROLL - ARMS CROSSED ON CHEST
        # Detection: Wrists are close together AND in front of body center
        # Both wrists should be near chest level (between shoulders and elbows)
        wrists_close = current_wrist_distance < self.neutral_wrist_distance * 0.4  # Wrists very close
        wrists_at_chest = (left_wrist.y > left_shoulder.y and left_wrist.y < left_elbow.y + 0.15 and
                          right_wrist.y > right_shoulder.y and right_wrist.y < right_elbow.y + 0.15)
        
        if wrists_close and wrists_at_chest:
            return 'roll'
        
        # PRIORITY 3: LEFT LANE - Lean body left
        if shoulder_center_x < self.neutral_shoulder_x - self.lean_threshold:
            return 'left'
        
        # PRIORITY 4: RIGHT LANE - Lean body right
        if shoulder_center_x > self.neutral_shoulder_x + self.lean_threshold:
            return 'right'
        
        # No clear gesture detected
        return None
    
    def execute_action(self, action):
        """
        Single tap for left/right, with individual cooldowns per action.
        """
        if not action:
            return
            
        current_time = time.time()
        
        # Check cooldown for this specific action
        if current_time - self.last_action_time[action] < self.action_cooldowns[action]:
            return  # Too soon for this action
        
        if action == 'jump':
            pyautogui.press('up', interval=0.1)
            print("⬆️  JUMP!")
            
        elif action == 'roll':
            pyautogui.press('down', interval=0.1)
            print("⬇️  ROLL!")
            
        elif action == 'left':
            pyautogui.press('left', interval=0.1)
            print("⬅️  LEFT LANE")
            
        elif action == 'right':
            pyautogui.press('right', interval=0.1)
            print("➡️  RIGHT LANE")
        
        # Update last action time for this specific action
        self.last_action_time[action] = current_time
    
    def draw_info(self, frame, action, fps):
        """
        Draw helpful information on the video feed.
        """
        h, w, _ = frame.shape
        
        # Show current action in big green text
        if action:
            cv2.putText(frame, f"ACTION: {action.upper()}", (10, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        
        # Show FPS (processing speed)
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show calibration status
        status = "CALIBRATED ✓" if self.calibrated else "CALIBRATING..."
        color = (0, 255, 0) if self.calibrated else (0, 165, 255)
        cv2.putText(frame, status, (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Instructions
        instructions = [
            "CONTROLS:",
            "Raise arms UP = JUMP",
            "CROSS ARMS on chest = ROLL",
            "Lean LEFT = LEFT LANE",
            "Lean RIGHT = RIGHT LANE",
            "",
            "Press 'Q' to quit",
            "Press 'R' to recalibrate"
        ]
        
        y_offset = 30
        for i, text in enumerate(instructions):
            if "CROSS ARMS" in text:
                cv2.putText(frame, text, (w - 400, y_offset + i*30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            else:
                cv2.putText(frame, text, (w - 400, y_offset + i*30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        return frame
    
    def run(self):
        """
        Main program loop.
        """
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("=" * 60)
        print("🎮 SUBWAY SURFERS - CROSS ARMS VERSION")
        print("=" * 60)
        print("\n🎯 CONTROLS:")
        print("   ⬆️  Raise both arms UP → JUMP")
        print("   ❌  CROSS ARMS on chest → ROLL (EASY!)")
        print("   ⬅️  Lean body left → MOVE LEFT")
        print("   ➡️  Lean body right → MOVE RIGHT")
        print("\nStarting in 5 seconds...\n")
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        print("\n🚀 CONTROLLER ACTIVE!\n")
        time.sleep(2)
        
        prev_time = 0
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time
            
            action = None
            
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                action = self.detect_gesture(results.pose_landmarks.landmark)
                
                if action:
                    self.execute_action(action)
            else:
                cv2.putText(frame, "NO PERSON DETECTED", (10, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            frame = self.draw_info(frame, action, fps)
            cv2.imshow('Subway Surfers - CROSS ARMS', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.calibrated = False
                print("\n🔄 Recalibrating...")
        
        cap.release()
        cv2.destroyAllWindows()
        print("\n👋 Controller stopped!")


if __name__ == "__main__":
    print("\n🎮 CROSS ARMS VERSION - Roll by crossing arms on chest!\n")
    controller = SubwaySurfersController()
    controller.run()