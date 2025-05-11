import tkinter as tk
from tkinter import ttk

class StudyTrackerGUI:
    def __init__(self, tracker):
        self.tracker = tracker
        
        self.root = tk.Tk()
        self.root.title("Study Tracker")
        self.setup_gui()
    
    def setup_gui(self):
        stats_frame = ttk.LabelFrame(self.root, text="Stats")
        stats_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.study_time_label = ttk.Label(stats_frame, text="Study Time: 0:00:00")
        self.study_time_label.pack()
        
        self.points_label = ttk.Label(stats_frame, text="Points: 0")
        self.points_label.pack()
        
        self.level_label = ttk.Label(stats_frame, text="Level: 1")
        self.level_label.pack()
        
        self.export_button = ttk.Button(stats_frame, text="Export Stats", 
                                       command=self.tracker.export_stats)
        self.export_button.pack(pady=5)
        
        pomo_frame = ttk.LabelFrame(self.root, text="Pomodoro")
        pomo_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.pomo_label = ttk.Label(pomo_frame, text="25:00")
        self.pomo_label.pack()
        
        self.pomo_button = ttk.Button(pomo_frame, text="Start Pomodoro",
                                    command=self.tracker.pomodoro.toggle)
        self.pomo_button.pack()
    
    def update_gui(self):
        self.points_label.config(text=f"Points: {self.tracker.points}")
        self.level_label.config(text=f"Level: {self.tracker.level}")
        
        hours, remainder = divmod(int(self.tracker.study_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = f"{hours}:{minutes:02d}:{seconds:02d}"
        self.study_time_label.config(text=f"Study Time: {time_string}")
        
        self.root.after(1000, self.update_gui)
