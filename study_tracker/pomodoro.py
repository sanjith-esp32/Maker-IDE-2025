import threading
import time

class PomodoroTimer:
    def __init__(self, tracker):
        self.tracker = tracker
        self.active = False
        self.pomodoro_time = 25 * 60  # 25 minutes
        self.break_time = 5 * 60  # 5 minutes
    
    def toggle(self):
        if not self.active:
            self.active = True
            # Make sure gui exists before trying to access it
            if hasattr(self.tracker, 'gui'):
                self.tracker.gui.pomo_button.config(text="Stop Pomodoro")
            threading.Thread(target=self.run).start()
        else:
            self.active = False
            if hasattr(self.tracker, 'gui'):
                self.tracker.gui.pomo_button.config(text="Start Pomodoro")
    
    def play_notification(self, is_break=False):
        try:
            self.tracker.beep()
        except Exception as e:
            print(f"Could not play beep: {e}")
    
    def run(self):
        while self.active:
            remaining = self.pomodoro_time
            while remaining > 0 and self.active:
                mins, secs = divmod(remaining, 60)
                if hasattr(self.tracker, 'gui'):
                    self.tracker.gui.pomo_label.config(text=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                remaining -= 1
            
            if self.active:
                self.tracker.add_points(50)
                self.play_notification()
                
                remaining = self.break_time
                while remaining > 0 and self.active:
                    mins, secs = divmod(remaining, 60)
                    if hasattr(self.tracker, 'gui'):
                        self.tracker.gui.pomo_label.config(text=f"Break: {mins:02d}:{secs:02d}")
                    time.sleep(1)
                    remaining -= 1
                
                if self.active:
                    self.play_notification(is_break=True)

            if hasattr(self.tracker, 'gui'):
                self.tracker.gui.pomo_label.config(text="25:00")
            self.active = False
            if hasattr(self.tracker, 'gui'):
                self.tracker.gui.pomo_button.config(text="Start Pomodoro")
