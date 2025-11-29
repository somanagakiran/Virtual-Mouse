"""Virtual Mouse - Main Application
This module implements a virtual mouse system using hand gesture recognition.
"""

import cv2
import numpy as np
import pyautogui
from hand_detection import HandDetector
from gesture_recognition import GestureRecognizer
from mouse_control import MouseController
import time

class VirtualMouse:
    def __init__(self):
        self.hand_detector = HandDetector()
        self.gesture_recognizer = GestureRecognizer()
        self.mouse_controller = MouseController()
        self.camera = cv2.VideoCapture(0)
        self.fps = 30
        self.frame_width = 1280
        self.frame_height = 720
        
    def run(self):
        """Main application loop"""
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break
                
            # Flip the frame for selfie view
            frame = cv2.flip(frame, 1)
            
            # Detect hands in the frame
            hands = self.hand_detector.detect(frame)
            
            if hands:
                hand = hands[0]
                # Recognize gesture from hand landmarks
                gesture = self.gesture_recognizer.recognize(hand)
                
                # Get hand position for mouse movement
                x, y = self.hand_detector.get_position(hand)
                
                # Control mouse based on gesture
                self.handle_gesture(gesture, x, y, frame)
            
            # Display frame
            cv2.imshow('Virtual Mouse', frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cleanup()
    
    def handle_gesture(self, gesture, x, y, frame):
        """Handle mouse control based on recognized gesture"""
        screen_x = int(x * 1920 / self.frame_width)
        screen_y = int(y * 1080 / self.frame_height)
        
        if gesture == 'move':
            self.mouse_controller.move(screen_x, screen_y)
        elif gesture == 'click':
            self.mouse_controller.click(screen_x, screen_y)
        elif gesture == 'right_click':
            self.mouse_controller.right_click(screen_x, screen_y)
        elif gesture == 'drag':
            self.mouse_controller.drag(screen_x, screen_y)
        elif gesture == 'scroll_up':
            self.mouse_controller.scroll_up()
        elif gesture == 'scroll_down':
            self.mouse_controller.scroll_down()
    
    def cleanup(self):
        """Clean up resources"""
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = VirtualMouse()
    app.run()
