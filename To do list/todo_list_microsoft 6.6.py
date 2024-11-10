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
        
        # Initialize task counter and lists
        self.task_count = 0
        self.task_vars = []  # Store checkbox variables for each task
        self.progress_labels = []  # Store progress labels
        self.task_reward_pairs = []  # Store task-reward pairs
        self.task_names = []  # Store task names
        self.weekly_goals = []  # Store weekly goals
        
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
        # Create navigation buttons at top
        nav_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)
        
        self.tasks_button = ttk.Button(nav_frame, text="Tasks", command=self.show_tasks_page)
        self.tasks_button.pack(side="left", padx=5)
        
        self.progress_button = ttk.Button(nav_frame, text="Progress", command=self.show_progress_page)
        self.progress_button.pack(side="left", padx=5)

        self.history_button = ttk.Button(nav_frame, text="History", command=self.show_history_page)
        self.history_button.pack(side="left", padx=5)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create pages
        self.tasks_page = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        self.progress_page = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        self.history_page = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        
        # Tasks page layout
        # Task-Reward mapping section first
        self.reward_mapping_frame = ttk.Frame(self.tasks_page, style="Tracker.TFrame")
        self.reward_mapping_frame.pack(fill="x", pady=(0, 20))
        
        rewards_label = ttk.Label(
            self.reward_mapping_frame,
            text="Task-Reward Mapping",
            style="Header.TLabel"
        )
        rewards_label.pack(fill="x")

        # Create a frame for task-reward pairs
        self.reward_pairs_frame = ttk.Frame(self.reward_mapping_frame, style="Tracker.TFrame")
        self.reward_pairs_frame.pack(fill="x", pady=(10, 0))
        
        # Add initial task-reward pair
        self.add_task_reward_pair()

        # Add weekly goals section
        goals_label = ttk.Label(
            self.reward_mapping_frame,
            text="Weekly Goals",
            style="Header.TLabel"
        )
        goals_label.pack(fill="x", pady=(10, 0))
        
        # Frame for goals input and list
        goals_frame = ttk.Frame(self.reward_mapping_frame, style="Tracker.TFrame")
        goals_frame.pack(fill="x", pady=(10, 0))
        
        # Goals input field
        self.goals_entry = ttk.Entry(
            goals_frame,
            font=('Segoe UI', 10),
            width=50
        )
        self.goals_entry.pack(side="left", padx=5)
        
        # Add goal button
        add_goal_btn = ttk.Button(
            goals_frame,
            text="Add Goal",
            command=self.add_weekly_goal
        )
        add_goal_btn.pack(side="left", padx=5)
        
        # Goals list display
        self.goals_listbox = tk.Listbox(
            self.reward_mapping_frame,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=('Segoe UI', 10),
            height=6,
            selectmode=tk.SINGLE
        )
        self.goals_listbox.pack(fill="x", pady=5)
        
        # Delete goal button
        delete_goal_btn = ttk.Button(
            self.reward_mapping_frame,
            text="Delete Selected Goal",
            command=self.delete_weekly_goal
        )
        delete_goal_btn.pack(pady=5)
        
        # Main task tracker area
        self.tracker_frame = ttk.Frame(self.tasks_page, style="Tracker.TFrame")
        self.tracker_frame.pack(side="left", fill="both", expand=True)
        
        self.right_frame = ttk.Frame(self.tasks_page, style="Tracker.TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        # Create components
        self.create_dashboard()
        self.create_history_section()
        self.create_header()
        self.create_task_grid()
        
        # Show tasks page by default
        self.show_tasks_page()

    def add_weekly_goal(self):
        goal = self.goals_entry.get().strip()
        if goal:
            self.weekly_goals.append(goal)
            self.goals_listbox.insert(tk.END, f"• {goal}")
            self.goals_entry.delete(0, tk.END)
            
    def delete_weekly_goal(self):
        selection = self.goals_listbox.curselection()
        if selection:
            index = selection[0]
            self.weekly_goals.pop(index)
            self.goals_listbox.delete(index)