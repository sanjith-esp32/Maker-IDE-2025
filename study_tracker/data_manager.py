import os
import json
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'study_data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_session_data(self, data):
        today = datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(self.data_dir, f'session_{today}.txt')
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_session_data(self):
        today = datetime.now().strftime('%Y-%m-%d')
        file_path = os.path.join(self.data_dir, f'session_{today}.txt')
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                print("Error loading previous session data")
        
        return None
    
    def get_study_history(self):
        history = {}
        
        try:
            for filename in os.listdir(self.data_dir):
                if filename.startswith('session_') and filename.endswith('.txt'):
                    file_path = os.path.join(self.data_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            session_data = json.load(f)
                            date = session_data.get('date')
                            if date:
                                history[date] = session_data
                    except:
                        continue
        except Exception as e:
            print(f"Error reading study history: {e}")
            
        return history
    
    def check_and_reset_weekly_stats(self, current_year, current_week):
        try:
            weekly_files = []
            for filename in os.listdir(self.data_dir):
                if filename.startswith('weekly_stats_') and filename.endswith('.txt'):
                    weekly_files.append(filename)
            
            if not weekly_files:
                return
            
            weekly_files.sort(reverse=True)
            
            last_file = weekly_files[0]
            parts = last_file.replace('weekly_stats_', '').replace('.txt', '').split('_')
            if len(parts) >= 2:
                last_year = int(parts[0])
                last_week = int(parts[1].replace('week', ''))
                
                if last_year != current_year or last_week != current_week:
                    old_file_path = os.path.join(self.data_dir, last_file)
                    archived_path = os.path.join(
                        self.data_dir, 
                        f'weekly_stats_{last_year}_week{last_week}_completed.txt'
                    )
                    
                    if os.path.exists(old_file_path):
                        with open(old_file_path, 'r') as src:
                            content = src.read()
                        
                        with open(archived_path, 'w') as dest:
                            dest.write(content)
                            dest.write(f"\nWeek completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        
                        os.remove(old_file_path)
                        print(f"Weekly stats reset: archived week {last_week} of {last_year}")
                    
        except Exception as e:
            print(f"Error checking weekly stats: {e}")
    
    def export_stats(self, study_time, points, level, session_start_time):
        today = datetime.now()
        year, week_num, _ = today.isocalendar()
        weekly_stats_file = os.path.join(self.data_dir, f'weekly_stats_{year}_week{week_num}.txt')
        
        self.check_and_reset_weekly_stats(year, week_num)
        
        try:
            weekly_totals = {
                'total_time': 0,
                'total_points': 0,
                'sessions': 0,
                'week_start': None
            }
            
            if os.path.exists(weekly_stats_file):
                try:
                    with open(weekly_stats_file, 'r') as f:
                        for line in f:
                            if line.startswith("Total accumulated study time:"):
                                time_parts = line.split(": ")[1].strip().split(":")
                                hours = int(time_parts[0])
                                minutes = int(time_parts[1])
                                seconds = int(time_parts[2])
                                weekly_totals['total_time'] = hours * 3600 + minutes * 60 + seconds
                            elif line.startswith("Total points earned:"):
                                weekly_totals['total_points'] = int(line.split(": ")[1].strip())
                            elif line.startswith("Number of study sessions:"):
                                weekly_totals['sessions'] = int(line.split(": ")[1].strip())
                            elif line.startswith("Week starting:"):
                                weekly_totals['week_start'] = line.split(": ")[1].strip()
                except Exception as e:
                    print(f"Error reading weekly stats: {e}")
            
            weekly_totals['total_time'] += int(study_time)
            weekly_totals['total_points'] += points
            weekly_totals['sessions'] += 1
            
            if not weekly_totals['week_start']:
                week_start = today - timedelta(days=today.weekday())
                weekly_totals['week_start'] = week_start.strftime('%Y-%m-%d')
            
            total_hours, remainder = divmod(weekly_totals['total_time'], 3600)
            total_minutes, total_seconds = divmod(remainder, 60)
            total_time_string = f"{total_hours}:{total_minutes:02d}:{total_seconds:02d}"
            
            hours, remainder = divmod(int(study_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_string = f"{hours}:{minutes:02d}:{seconds:02d}"
            
            with open(weekly_stats_file, 'w') as f:
                f.write("===== WEEKLY STUDY STATISTICS =====\n\n")
                f.write(f"Report generated: {today.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Week starting: {weekly_totals['week_start']}\n")
                f.write(f"Year: {year}, Week number: {week_num}\n\n")
                
                f.write(f"Total accumulated study time: {total_time_string}\n")
                f.write(f"Total points earned: {weekly_totals['total_points']}\n")
                f.write(f"Number of study sessions: {weekly_totals['sessions']}\n\n")
                
                f.write(f"Current Study Session:\n")
                f.write(f"- Study time: {time_string}\n")
                f.write(f"- Points earned: {points}\n")
                f.write(f"- Current level: {level}\n")
                f.write(f"- Session started: {session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                history_data = self.get_study_history()
                if history_data:
                    f.write("This Week's Study Sessions:\n")
                    for date, data in history_data.items():
                        date_obj = datetime.strptime(date, '%Y-%m-%d')
                        date_year, date_week, _ = date_obj.isocalendar()
                        if date_year == year and date_week == week_num:
                            hours, remainder = divmod(int(data.get('study_time', 0)), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            hist_time = f"{hours}:{minutes:02d}:{seconds:02d}"
                            f.write(f"- {date}: {hist_time} studied, {data.get('points', 0)} points, level {data.get('level', 1)}\n")
            
            print(f"Weekly study statistics exported to {weekly_stats_file}")
            
        except Exception as e:
            print(f"Error exporting weekly statistics: {e}")
