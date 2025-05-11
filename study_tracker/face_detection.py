import cv2
import mediapipe as mp
import time
import numpy as np

class FaceDetector:
    def __init__(self, status_callback):
        self.status_callback = status_callback
        self.is_studying = False
        
        # Initialize face mesh
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def start_monitoring(self):
        print("Initializing camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Failed to open default camera, trying alternative...")
            cap = cv2.VideoCapture(2)
        
        if not cap.isOpened():
            print("No camera available. Operating in camera-less mode.")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        last_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to grab frame")
                    time.sleep(0.1)
                    continue
                
                current_time = time.time()
                time_diff = current_time - last_time
                last_time = current_time
                
                self.process_frame(frame, time_diff)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        except KeyboardInterrupt:
            print("\nDetected keyboard interrupt. Shutting down...")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Camera resources released")
    
    def process_frame(self, frame, time_diff):
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            previous_state = self.is_studying
            h, w, _ = frame.shape
            
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                
                # Get key facial landmarks
                nose_tip = face_landmarks.landmark[4]  # Nose tip
                left_eye = face_landmarks.landmark[33]  # Left eye
                right_eye = face_landmarks.landmark[263]  # Right eye
                forehead = face_landmarks.landmark[10]  # Forehead
                chin = face_landmarks.landmark[152]  # Chin
                
                # Draw key points for debugging
                nose_x, nose_y = int(nose_tip.x * w), int(nose_tip.y * h)
                cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)  # Green for nose
                
                left_eye_x, left_eye_y = int(left_eye.x * w), int(left_eye.y * h)
                right_eye_x, right_eye_y = int(right_eye.x * w), int(right_eye.y * h)
                cv2.circle(frame, (left_eye_x, left_eye_y), 3, (0, 0, 255), -1)  # Red for eyes
                cv2.circle(frame, (right_eye_x, right_eye_y), 3, (0, 0, 255), -1)
                
                # Calculate vertical angle (looking up/down)
                # When looking down, the nose-to-forehead distance increases relative to the nose-to-chin distance
                forehead_y = int(forehead.y * h)
                chin_y = int(chin.y * h)
                
                vertical_ratio = (nose_y - forehead_y) / (chin_y - nose_y) if (chin_y - nose_y) > 0 else 0
                
                # Calculate horizontal angle (looking left/right)
                # We measure symmetry between left eye-nose and right eye-nose
                left_dist = abs(left_eye_x - nose_x)
                right_dist = abs(right_eye_x - nose_x)
                horizontal_ratio = min(left_dist, right_dist) / max(left_dist, right_dist) if max(left_dist, right_dist) > 0 else 0
                
                # Additional check for nose position in frame - should be in lower half when looking down
                nose_position_ratio = nose_y / h
                is_nose_lower = nose_position_ratio > 0.55  # Nose should be in lower half of frame when looking down
                
                # Thresholds for classification - increased threshold for vertical detection
                looking_down = vertical_ratio > 0.85 and is_nose_lower  # Made this stricter AND added position check
                
                # Tolerance for left/right movement
                looking_straight = horizontal_ratio > 0.5
                
                # Determine if studying
                if looking_down and looking_straight:
                    if not self.is_studying:
                        print("Started studying")
                    self.is_studying = True
                else:
                    if self.is_studying:
                        reason = "not looking down enough" if not looking_down else "looking too far sideways"
                        print(f"Stopped studying: {reason}")
                    self.is_studying = False
                
                # Display debug info
                cv2.putText(frame, f"Vert ratio: {vertical_ratio:.2f}", (10, 110), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                cv2.putText(frame, f"Horiz ratio: {horizontal_ratio:.2f}", (10, 130), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                cv2.putText(frame, f"Nose Y pos: {nose_position_ratio:.2f}", (10, 150), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                cv2.putText(frame, f"Looking down: {looking_down}", (10, 170), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                cv2.putText(frame, f"Looking straight: {looking_straight}", (10, 190), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                
            else:
                if self.is_studying:
                    print("No face detected, stopped studying")
                self.is_studying = False
            
            # Call the callback with the current status
            self.status_callback(self.is_studying, time_diff)
            
            # Draw overall status on frame
            status_text = "Studying" if self.is_studying else "Not Studying"
            cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            try:
                cv2.putText(frame, f"Points: {self.status_callback.__self__.points}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            except:
                # In case points are not accessible
                pass
            
            cv2.imshow('Study Tracker', frame)
        except Exception as e:
            print(f"Error processing face: {e}")
