import tkinter as tk
from tkinter import ttk, PhotoImage
import os
from datetime import timedelta

class StudyTrackerGUI:
    def __init__(self, tracker):
        self.tracker = tracker
        
        self.root = tk.Tk()  # We'll create a custom dark theme
        self.root.title("Study Tracker Pro")
        self.root.geometry("450x650")
        self.root.configure(bg="#1E1E2E")
        self.set_window_icon()
        self.setup_styles()
        self.setup_gui()
    
    def set_window_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "assets", "study_icon.png")
            if os.path.exists(icon_path):
                icon = PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
        except:
            pass  # Silently fail if icon doesn't exist
    
    def setup_styles(self):
        # Configure colors for a more vibrant dark theme
        self.colors = {
            "bg": "#1E1E2E",            # Dark background
            "frame_bg": "#2D2D3F",      # Slightly lighter for frames
            "text": "#CDD6F4",          # Light text color
            "accent": "#89B4FA",        # Soft blue accent
            "accent2": "#F5C2E7",       # Secondary accent (pink)
            "button": "#45475A",        # Button background
            "progress_bg": "#313244",   # Progress bar background
            "progress_fg": "#89B4FA",   # Progress bar foreground
            "highlight": "#F9E2AF"      # Highlight color (yellow)
        }
        
        # Configure the ttk styles
        style = ttk.Style()
        
        # Frame styling
        style.configure("TFrame", background=self.colors["frame_bg"])
        style.configure("TLabelframe", background=self.colors["frame_bg"], foreground=self.colors["text"])
        style.configure("TLabelframe.Label", background=self.colors["bg"], foreground=self.colors["text"], 
                        font=("Helvetica", 11, "bold"))
        
        # Label styling
        style.configure("TLabel", background=self.colors["frame_bg"], foreground=self.colors["text"], 
                        font=("Helvetica", 10))
        style.configure("Header.TLabel", background=self.colors["frame_bg"], foreground=self.colors["text"], 
                        font=("Helvetica", 12, "bold"))
        style.configure("Value.TLabel", background=self.colors["frame_bg"], foreground=self.colors["accent"], 
                        font=("Helvetica", 11))
        style.configure("Title.TLabel", background=self.colors["bg"], foreground=self.colors["accent"], 
                        font=("Helvetica", 16, "bold"))
        style.configure("Timer.TLabel", background=self.colors["frame_bg"], foreground=self.colors["highlight"], 
                        font=("Helvetica", 32, "bold"))
        
        # Button styling
        style.configure("TButton", background=self.colors["button"], foreground=self.colors["text"], 
                        borderwidth=1, font=("Helvetica", 10))
        style.map("TButton",
                 background=[("active", self.colors["accent"])],
                 foreground=[("active", self.colors["bg"])])
        
        style.configure("Accent.TButton", background=self.colors["accent"], foreground=self.colors["bg"], 
                        font=("Helvetica", 11, "bold"))
        style.map("Accent.TButton",
                 background=[("active", self.colors["accent2"])],
                 foreground=[("active", self.colors["bg"])])
        
        style.configure("Secondary.TButton", background=self.colors["button"], foreground=self.colors["text"], 
                        font=("Helvetica", 9))
        
        # Separator styling
        style.configure("TSeparator", background=self.colors["accent"])
        
        # Progress bar styling
        style.configure("TProgressbar", background=self.colors["progress_fg"], troughcolor=self.colors["progress_bg"], 
                        borderwidth=0, thickness=8)
    
    def setup_gui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=15, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(main_container, text="Study Tracker Pro", style="Title.TLabel", background=self.colors["bg"])
        title_label.pack(pady=(0, 15))
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_container, text="Statistics", padding="15")
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Study time
        time_frame = ttk.Frame(stats_frame)
        time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(time_frame, text="Total Study Time:", style="Header.TLabel").pack(side=tk.LEFT)
        self.study_time_label = ttk.Label(time_frame, text="0:00:00", style="Value.TLabel")
        self.study_time_label.pack(side=tk.RIGHT)
        
        ttk.Separator(stats_frame, orient='horizontal').pack(fill=tk.X, pady=8)
        
        # Points and level
        points_frame = ttk.Frame(stats_frame)
        points_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(points_frame, text="Points:", style="Header.TLabel").pack(side=tk.LEFT)
        self.points_label = ttk.Label(points_frame, text="0", style="Value.TLabel")
        self.points_label.pack(side=tk.RIGHT)
        
        # Level with progress bar
        level_frame = ttk.Frame(stats_frame)
        level_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(level_frame, text="Level:", style="Header.TLabel").pack(side=tk.LEFT)
        self.level_label = ttk.Label(level_frame, text="1", style="Value.TLabel")
        self.level_label.pack(side=tk.RIGHT)
        
        # Progress to next level
        progress_frame = ttk.Frame(stats_frame)
        progress_frame.pack(fill=tk.X, pady=(8, 5))
        
        ttk.Label(progress_frame, text="Progress to next level:", style="TLabel").pack(anchor="w")
        self.level_progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        self.level_progress.pack(fill=tk.X, pady=(5, 0))
        self.level_progress["value"] = 65  # Will be updated dynamically
        
        # Export button with tooltip
        button_frame = ttk.Frame(stats_frame)
        button_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.export_button = ttk.Button(button_frame, text="Export Statistics", 
                                      command=self.tracker.export_stats)
        self.export_button.pack(side=tk.RIGHT)
        self.create_tooltip(self.export_button, "Export your study data to a file")
        
        # Pomodoro frame
        pomo_frame = ttk.LabelFrame(main_container, text="Pomodoro Timer", padding="15")
        pomo_frame.pack(fill=tk.X, pady=15)
        
        # Timer display
        self.pomo_label = ttk.Label(pomo_frame, text="25:00", style="Timer.TLabel")
        self.pomo_label.pack(pady=10, anchor=tk.CENTER)
        
        # Session info
        self.session_label = ttk.Label(pomo_frame, text="Ready to start", style="TLabel")
        self.session_label.pack(pady=(0, 10), anchor=tk.CENTER)
        
        # Timer controls
        controls_frame = ttk.Frame(pomo_frame)
        controls_frame.pack(fill=tk.X)
        
        self.pomo_button = ttk.Button(controls_frame, text="Start Focus Session",
                                   command=self.tracker.pomodoro.toggle,
                                   style="Accent.TButton")
        self.pomo_button.pack(pady=5, fill=tk.X)
        
        button_frame = ttk.Frame(pomo_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.reset_button = ttk.Button(button_frame, text="Reset Timer", 
                                     command=self.reset_timer, 
                                     style="Secondary.TButton")
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.skip_button = ttk.Button(button_frame, text="Skip Break", 
                                    command=self.skip_break, 
                                    style="Secondary.TButton")
        self.skip_button.pack(side=tk.RIGHT, padx=5)
        self.skip_button["state"] = "disabled"  # Initially disabled
        
        # Daily goals frame
        goals_frame = ttk.LabelFrame(main_container, text="Daily Goals", padding="15")
        goals_frame.pack(fill=tk.X, pady=10)
        
        # Goal progress
        goal_label = ttk.Label(goals_frame, text="Study Time Goal: 2 hours", style="TLabel")
        goal_label.pack(anchor="w")
        
        self.goal_progress = ttk.Progressbar(goals_frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        self.goal_progress.pack(fill=tk.X, pady=5)
        
        goal_time_frame = ttk.Frame(goals_frame)
        goal_time_frame.pack(fill=tk.X)
        
        ttk.Label(goal_time_frame, text="0:00", style="TLabel").pack(side=tk.LEFT)
        ttk.Label(goal_time_frame, text="2:00:00", style="TLabel").pack(side=tk.RIGHT)
        
        # Initial GUI update
        self.update_gui()
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget with the given text"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=text, background=self.colors["frame_bg"],
                          foreground=self.colors["text"], relief="solid", borderwidth=1,
                          font=("Helvetica", "9", "normal"), padx=5, pady=2)
            label.pack()
            
        def leave(event):
            if hasattr(self, "tooltip"):
                self.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def reset_timer(self):
        # This method would be implemented to reset the Pomodoro timer
        if hasattr(self.tracker.pomodoro, 'reset'):
            self.tracker.pomodoro.reset()
        self.pomo_label.config(text="25:00")
        self.session_label.config(text="Ready to start")
        self.pomo_button.config(text="Start Focus Session")
        self.skip_button["state"] = "disabled"
    
    def skip_break(self):
        # This method would be implemented to skip break time
        if hasattr(self.tracker.pomodoro, 'skip_break'):
            self.tracker.pomodoro.skip_break()
        self.skip_button["state"] = "disabled"
    
    def update_gui(self):
        # Update points and level
        self.points_label.config(text=f"{self.tracker.points}")
        self.level_label.config(text=f"{self.tracker.level}")
        
        # Update study time display
        time_delta = timedelta(seconds=int(self.tracker.study_time))
        time_string = str(time_delta)
        if time_string.startswith('0:'):  # Remove leading '0:' for times less than 1 hour
            time_string = time_string[2:]
        self.study_time_label.config(text=time_string)
        
        # Update progress bars
        # Level progress (assuming we know points needed for next level)
        points_for_level = 100  # This should be calculated based on current level
        current_level_points = self.tracker.points % points_for_level
        level_progress = (current_level_points / points_for_level) * 100
        self.level_progress["value"] = level_progress
        
        # Goal progress (assuming 2 hour daily goal)
        daily_goal_seconds = 7200  # 2 hours in seconds
        daily_progress = min((self.tracker.study_time / daily_goal_seconds) * 100, 100)
        self.goal_progress["value"] = daily_progress
        
        # Schedule the next update
        self.root.after(1000, self.update_gui)
