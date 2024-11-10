import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime
import numpy as np

class WeeklyTaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Task Tracker")
        self.root.geometry("1400x800")  # Increased width for dashboard
        
        # Initialize task history
        self.task_history = {}
        self.load_task_history()
        
        # Apply modern styles
        self.apply_styles()
        
        # Create main layout
        self.create_layout()
        
    def apply_styles(self):
        self.colors = {
            'primary': '#FFD700',      # Yellow
            'secondary': '#808080',     # Grey
            'background': '#000000',    # Black
            'surface': '#1A1A1A',       # Dark grey
            'text': '#FFFFFF',          # White text
            'border': '#404040',        # Dark grey border
            'progress': '#4CAF50',      # Green for progress
            'chart_bg': '#2D2D2D'       # Dark grey for chart background
        }
        
        style = ttk.Style()
        
        # Configure frame styles
        style.configure(
            "Tracker.TFrame",
            background=self.colors['background']
        )
        
        # Configure label styles
        style.configure(
            "Header.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            font=('Segoe UI', 12, 'bold'),
            padding=10
        )
        
        style.configure(
            "Day.TLabel",
            background=self.colors['primary'],
            foreground='black',
            font=('Segoe UI', 11, 'bold'),
            padding=8
        )

        style.configure(
            "Progress.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['progress'],
            font=('Segoe UI', 10)
        )

        style.configure(
            "History.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10)
        )
        
    def create_layout(self):
        # Main container with two columns
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left column for tracker
        self.tracker_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        self.tracker_frame.pack(side="left", fill="both", expand=True)
        
        # Right column for dashboard and history
        self.right_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        # Dashboard section
        self.dashboard_frame = ttk.Frame(self.right_frame, style="Tracker.TFrame")
        self.dashboard_frame.pack(fill="both", expand=True)
        
        # History section
        self.history_frame = ttk.Frame(self.right_frame, style="Tracker.TFrame")
        self.history_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Create components in correct order
        self.create_dashboard()
        self.create_history_section()
        self.create_header()
        self.create_task_grid()
        self.create_goals_section()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()