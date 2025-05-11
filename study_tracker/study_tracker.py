import threading
import time
from datetime import datetime
import os

from face_detection import FaceDetector
from gui import StudyTrackerGUI
from data_manager import DataManager
from pomodoro import PomodoroTimer
from utils import create_beep_function

class StudyTracker:
    def __init__(self):
        # Initialize basic state
        self.study_time = 0
        self.points = 0
        self.level = 1
        self.is_studying = False
        self.point_accumulator = 0
        self.session_start_time = datetime.now()
        self.last_status_change = datetime.now()
        
        # Initialize components
        self.beep = create_beep_function()
        self.data_manager = DataManager()
        self.face_detector = FaceDetector(self.on_face_status_change)
        
        # Create pomodoro timer BEFORE GUI to avoid AttributeError
        self.pomodoro = PomodoroTimer(self)
        
        # Now create GUI after pomodoro is initialized
        self.gui = StudyTrackerGUI(self)
        
        # Load previous session data
        self.data_dir = os.path.join(os.path.dirname(__file__), 'study_data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_session_data()
        
        # Start background threads
        self.start_background_threads()
    
    def start_background_threads(self):
        # Start camera monitoring in a separate thread
        self.camera_thread = threading.Thread(target=self.face_detector.start_monitoring)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        
        # Start auto-save thread
        self.save_thread = threading.Thread(target=self.auto_save_data)
        self.save_thread.daemon = True
        self.save_thread.start()
    
    def on_face_status_change(self, is_studying, time_diff):
        self.is_studying = is_studying
        
        if is_studying:
            self.study_time += time_diff
            self.point_accumulator += time_diff
            if self.point_accumulator >= 1.0:
                points_to_add = int(self.point_accumulator)
                self.point_accumulator -= points_to_add
                self.add_points(points_to_add)
    
    def add_points(self, points):
        self.points += points
        if self.points >= self.level * 100:
            self.level_up()
        self.gui.update_gui()
    
    def level_up(self):
        self.level += 1
    
    def load_session_data(self):
        data = self.data_manager.load_session_data()
        if data:
            self.study_time = data.get('study_time', 0)
            self.points = data.get('points', 0)
            self.level = data.get('level', 1)
    
    def save_session_data(self):
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'study_time': self.study_time,
            'points': self.points,
            'level': self.level
        }
        self.data_manager.save_session_data(data)
    
    def auto_save_data(self):
        while True:
            time.sleep(300)  # Save every 5 minutes
            self.save_session_data()
    
    def export_stats(self):
        self.data_manager.export_stats(
            study_time=self.study_time,
            points=self.points,
            level=self.level,
            session_start_time=self.session_start_time
        )
    
    def run(self):
        self.gui.update_gui()
        try:
            self.gui.root.mainloop()
        finally:
            self.save_session_data()
            self.export_stats()
