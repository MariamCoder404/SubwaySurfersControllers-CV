import cv2
import mediapipe as mp
import pyautogui
import time

class HandGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.last_action = 0
        self.cooldown = 0.9
        
    def count_fingers(self, landmarks):
        """Count extended fingers"""
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        thumb_tip = 4
        
        fingers_up = 0
        
        # Thumb
        if landmarks[thumb_tip].x < landmarks[thumb_tip - 1].x:
            fingers_up += 1
        
        # Other fingers
        for tip in finger_tips:
            if landmarks[tip].y < landmarks[tip - 2].y:
                fingers_up += 1
        
        return fingers_up
    
    def get_hand_position(self, landmarks):
        """Get hand position (left, center, right)"""
        wrist = landmarks[0]
        
        if wrist.x < 0.3:
            return 'left'
        elif wrist.x > 0.7:
            return 'right'
        else:
            return 'center'
    
    def detect_gesture(self, landmarks):
        """Detect hand gesture"""
        fingers = self.count_fingers(landmarks)
        position = self.get_hand_position(landmarks)
        
        # 5 fingers = Jump
        if fingers == 5:
            return 'jump'
        
        # Fist (0 fingers) = Roll
        if fingers == 0:
            return 'roll'
        
        # Hand position for lane change
        if position == 'left':
            return 'left'
        elif position == 'right':
            return 'right'
        
        return None
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        print("🖐️ HAND GESTURE CONTROL")
        print("5 fingers → Jump")
        print("Fist → Roll")
        print("Move hand left/right → Change lane")
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    action = self.detect_gesture(hand_landmarks.landmark)
                    
                    if action and time.time() - self.last_action > self.cooldown:
                        if action == 'jump':
                            pyautogui.press('up')
                            print("⬆️ JUMP")
                        elif action == 'roll':
                            pyautogui.press('down')
                            print("⬇️ ROLL")
                        elif action == 'left':
                            pyautogui.press('left')
                            print("⬅️ LEFT")
                        elif action == 'right':
                            pyautogui.press('right')
                            print("➡️ RIGHT")
                        
                        self.last_action = time.time()
            
            cv2.imshow('Hand Gesture Control', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Create controller and run it
controller = HandGestureController()
controller.run()