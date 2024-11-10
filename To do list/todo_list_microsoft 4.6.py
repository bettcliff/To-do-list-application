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
        
        # Initialize task history and tracking
        self.task_history = {}
        self.task_tracking = {} # Track individual task progress
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
            'chart_bg': '#2D2D2D',      # Dark grey for chart background
            'low_progress': '#FF4444',  # Red for low progress
            'med_progress': '#FFBB33',  # Orange for medium progress
            'high_progress': '#00C851'  # Green for high progress
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

        # New styles for dashboard
        style.configure(
            "Dashboard.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10, 'bold'),
            padding=5
        )

        style.configure(
            "DashboardProgress.TLabel",
            background=self.colors['surface'],
            font=('Segoe UI', 9),
            padding=3
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

    def create_history_section(self):
        history_label = ttk.Label(
            self.history_frame,
            text="Task History",
            style="Header.TLabel"
        )
        history_label.pack(fill="x", pady=(0, 10))

        # Create scrollable history view
        history_canvas = tk.Canvas(
            self.history_frame,
            bg=self.colors['surface'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=history_canvas.yview)
        self.history_content = ttk.Frame(history_canvas, style="Tracker.TFrame")

        history_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        history_canvas.pack(side="left", fill="both", expand=True)
        history_canvas.create_window((0, 0), window=self.history_content, anchor="nw", width=history_canvas.winfo_width())

        self.history_content.bind("<Configure>", lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all")))
        
        self.display_task_history()

    def save_current_week(self):
        week_data = {
            'tasks': [],
            'progress': float(self.overall_progress_label.cget("text").split(":")[1].strip('%')),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        for task_id, task_info in self.task_tracking.items():
            task_text = task_info['description']
            task_progress = task_info['progress']
            week_data['tasks'].append({
                'description': task_text,
                'progress': task_progress,
                'daily_completion': task_info['daily_completion']
            })
            
        week_key = f"Week_{datetime.now().strftime('%Y_%W')}"
        self.task_history[week_key] = week_data
        self.save_task_history()
        self.display_task_history()

    def load_task_history(self):
        try:
            with open('task_history.json', 'r') as f:
                self.task_history = json.load(f)
        except FileNotFoundError:
            self.task_history = {}

    def save_task_history(self):
        with open('task_history.json', 'w') as f:
            json.dump(self.task_history, f)

    def display_task_history(self):
        # Clear existing history display
        for widget in self.history_content.winfo_children():
            widget.destroy()

        # Display each week's history
        for week_key, week_data in sorted(self.task_history.items(), reverse=True):
            week_frame = ttk.Frame(self.history_content, style="Tracker.TFrame")
            week_frame.pack(fill="x", pady=5)

            week_label = ttk.Label(
                week_frame,
                text=f"{week_key} ({week_data['date']})",
                style="History.TLabel"
            )
            week_label.pack(anchor="w")

            progress_label = ttk.Label(
                week_frame,
                text=f"Overall Progress: {week_data['progress']}%",
                style="History.TLabel"
            )
            progress_label.pack(anchor="w")

            for task in week_data['tasks']:
                if task['description']:  # Only show tasks with descriptions
                    task_label = ttk.Label(
                        week_frame,
                        text=f"• {task['description']}: {task['progress']}%",
                        style="History.TLabel"
                    )
                    task_label.pack(anchor="w", padx=(20, 0))

    def update_progress(self, task_id):
        if task_id in self.task_tracking:
            task_info = self.task_tracking[task_id]
            checked_count = sum(1 for checked in task_info['daily_completion'] if checked)
            percentage = int((checked_count / 7) * 100)
            task_info['progress'] = percentage
            
            # Update progress label
            row = task_info['row']
            self.progress_labels[row-1].configure(text=f"{percentage}%")
            
            # Update dashboard
            self.update_dashboard()
            
            # Save current week's progress
            self.save_current_week()

    def create_header(self):
        header_frame = ttk.Frame(self.tracker_frame, style="Tracker.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Date picker
        date_frame = ttk.Frame(header_frame, style="Tracker.TFrame")
        date_frame.pack(side="left", padx=10)
        
        date_label = ttk.Label(
            date_frame,
            text="Select Date:",
            style="Header.TLabel"
        )
        date_label.pack(side="left", padx=(0, 5))
        
        self.date_picker = DateEntry(
            date_frame,
            width=12,
            background=self.colors['surface'],
            foreground=self.colors['text'],
            borderwidth=2,
            command=self.update_date_info
        )
        self.date_picker.pack(side="left")
        
        # Month and week labels
        self.month_label = ttk.Label(
            header_frame,
            text=self.get_month_text(),
            style="Header.TLabel"
        )
        self.month_label.pack(side="left", padx=10)
        
        self.week_label = ttk.Label(
            header_frame,
            text=self.get_week_text(),
            style="Header.TLabel"
        )
        self.week_label.pack(side="left", padx=10)

        # Add overall progress label
        self.overall_progress_label = ttk.Label(
            header_frame,
            text="Overall Progress: 0%",
            style="Header.TLabel"
        )
        self.overall_progress_label.pack(side="right", padx=10)

    def get_month_text(self):
        selected_date = self.date_picker.get_date()
        return f"Month: {selected_date.strftime('%B %Y')}"
        
    def get_week_text(self):
        selected_date = self.date_picker.get_date()
        week_num = (selected_date.day - 1) // 7 + 1
        return f"Week {week_num}"
        
    def update_date_info(self):
        self.month_label.configure(text=self.get_month_text())
        self.week_label.configure(text=self.get_week_text())

    def create_task_grid(self):
        self.grid_frame = ttk.Frame(self.tracker_frame, style="Tracker.TFrame")
        self.grid_frame.pack(fill="both", expand=True)
        
        # Days of week headers
        days = ["Task", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Progress"]
        for i, day in enumerate(days):
            label = ttk.Label(
                self.grid_frame,
                text=day,
                style="Day.TLabel"
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Task rows
        self.task_vars = []  # Store checkbox variables for each task
        self.progress_labels = []  # Store progress labels
        for row in range(1, 16):
            # Task description
            task_entry = ttk.Entry(
                self.grid_frame,
                font=('Segoe UI', 10),
                style='Task.TEntry'
            )
            task_entry.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Checkboxes for each day
            row_vars = []
            for col in range(1, 8):
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(
                    self.grid_frame,
                    variable=var,
                    command=lambda r=row: self.update_progress(f"task_{r}")
                )
                checkbox.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                row_vars.append(var)
            self.task_vars.append(row_vars)
            
            # Progress label
            progress_label = ttk.Label(
                self.grid_frame,
                text="0%",
                style="Progress.TLabel"
            )
            progress_label.grid(row=row, column=8, sticky="nsew", padx=1, pady=1)
            self.progress_labels.append(progress_label)

    def create_goals_section(self):
        goals_frame = ttk.Frame(self.tracker_frame, style="Tracker.TFrame")
        goals_frame.pack(fill="x", pady=(0, 20))
        
        # Goals section
        goals_label = ttk.Label(
            goals_frame,
            text="Weekly Goals",
            style="Header.TLabel"
        )
        goals_label.pack(fill="x")
        
        self.goals_text = tk.Text(
            goals_frame,
            height=4,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=('Segoe UI', 10)
        )
        self.goals_text.pack(fill="x", pady=(10, 0))

        # Task-Reward mapping section
        rewards_frame = ttk.Frame(goals_frame, style="Tracker.TFrame")
        rewards_frame.pack(fill="x", pady=(20, 0))

        rewards_label = ttk.Label(
            rewards_frame,
            text="Task-Reward Mapping",
            style="Header.TLabel"
        )
        rewards_label.pack(fill="x")

        # Create a frame for task-reward pairs
        self.reward_pairs_frame = ttk.Frame(rewards_frame, style="Tracker.TFrame")
        self.reward_pairs_frame.pack(fill="x", pady=(10, 0))

        # Add single task-reward pair
        self.add_task_reward_pair()

    def add_task_reward_pair(self):
        # Clear existing pairs first
        for widget in self.reward_pairs_frame.winfo_children():
            widget.destroy()
            
        pair_frame = ttk.Frame(self.reward_pairs_frame, style="Tracker.TFrame")
        pair_frame.pack(fill="x", pady=5)

        task_entry = ttk.Entry(
            pair_frame,
            font=('Segoe UI', 10),
            width=30
        )
        task_entry.insert(0, "Enter task...")
        task_entry.bind('<FocusIn>', lambda e: task_entry.delete(0, 'end') if task_entry.get() == "Enter task..." else None)
        task_entry.bind('<FocusOut>', lambda e: task_entry.insert(0, "Enter task...") if task_entry.get() == "" else None)
        task_entry.pack(side="left", padx=5)

        ttk.Label(
            pair_frame,
            text="→",
            style="Header.TLabel"
        ).pack(side="left", padx=5)

        reward_entry = ttk.Entry(
            pair_frame,
            font=('Segoe UI', 10),
            width=30
        )
        reward_entry.insert(0, "Enter reward...")
        reward_entry.bind('<FocusIn>', lambda e: reward_entry.delete(0, 'end') if reward_entry.get() == "Enter reward..." else None)
        reward_entry.bind('<FocusOut>', lambda e: reward_entry.insert(0, "Enter reward...") if reward_entry.get() == "" else None)
        reward_entry.pack(side="left", padx=5)

        # Add button to add task to main area
        add_button = ttk.Button(
            pair_frame,
            text="Add to Tasks",
            command=lambda: self.add_to_main_tasks(task_entry, reward_entry)
        )
        add_button.pack(side="left", padx=5)

    def add_to_main_tasks(self, task_entry, reward_entry):
        # Get task text
        task_text = task_entry.get()
        if task_text and task_text != "Enter task...":
            # Find first empty task row
            for i in range(15):
                main_task_entry = self.grid_frame.grid_slaves(row=i+1, column=0)[0]
                if not main_task_entry.get():
                    main_task_entry.delete(0, 'end')
                    main_task_entry.insert(0, task_text)
                    
                    # Initialize task tracking
                    task_id = f"task_{i+1}"
                    self.task_tracking[task_id] = {
                        'description': task_text,
                        'progress': 0,
                        'daily_completion': [False] * 7,
                        'row': i+1
                    }
                    break
            
            # Clear entries
            task_entry.delete(0, 'end')
            task_entry.insert(0, "Enter task...")
            reward_entry.delete(0, 'end')
            reward_entry.insert(0, "Enter reward...")

    def create_dashboard(self):
        dashboard_label = ttk.Label(
            self.dashboard_frame,
            text="Task Progress Dashboard",
            style="Header.TLabel"
        )
        dashboard_label.pack(fill="x", pady=(0, 10))

        # Create scrollable frame for task progress
        canvas = tk.Canvas(
            self.dashboard_frame,
            bg=self.colors['surface'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(self.dashboard_frame, orient="vertical", command=canvas.yview)
        self.progress_frame = ttk.Frame(canvas, style="Tracker.TFrame")

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create window inside canvas
        canvas.create_window((0, 0), window=self.progress_frame, anchor="nw", width=canvas.winfo_width())
        self.progress_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add overall statistics section
        stats_frame = ttk.Frame(self.progress_frame, style="Tracker.TFrame")
        stats_frame.pack(fill="x", pady=10, padx=10)

        self.stats_label = ttk.Label(
            stats_frame,
            text="Overall Statistics",
            style="Dashboard.TLabel"
        )
        self.stats_label.pack(anchor="w")

        # Create progress bars container
        self.progress_bars_frame = ttk.Frame(self.progress_frame, style="Tracker.TFrame")
        self.progress_bars_frame.pack(fill="both", expand=True, padx=10)

    def update_dashboard(self):
        # Clear existing progress bars
        for widget in self.progress_bars_frame.winfo_children():
            widget.destroy()

        # Calculate overall statistics
        total_tasks = len(self.task_tracking)
        if total_tasks > 0:
            completed_tasks = sum(1 for task in self.task_tracking.values() if task['progress'] == 100)
            avg_progress = sum(task['progress'] for task in self.task_tracking.values()) / total_tasks
            
            stats_text = f"Total Tasks: {total_tasks}\n"
            stats_text += f"Completed Tasks: {completed_tasks}\n"
            stats_text += f"Average Progress: {avg_progress:.1f}%"
            self.stats_label.configure(text=stats_text)
            
            # Update overall progress label
            self.overall_progress_label.configure(text=f"Overall Progress: {avg_progress:.1f}%")

        # Create progress bar for each task
        for task_id, task_info in self.task_tracking.items():
            if task_info['description']:  # Only show tasks with descriptions
                task_frame = ttk.Frame(self.progress_bars_frame, style="Tracker.TFrame")
                task_frame.pack(fill="x", pady=5)

                # Task description
                task_label = ttk.Label(
                    task_frame,
                    text=task_info['description'],
                    style="Dashboard.TLabel"
                )
                task_label.pack(anchor="w")

                # Progress bar background
                bar_bg = tk.Canvas(
                    task_frame,
                    height=20,
                    bg=self.colors['surface'],
                    highlightthickness=0
                )
                bar_bg.pack(fill="x", pady=(2, 5))

                # Calculate progress bar color based on progress
                progress = task_info['progress']
                if progress < 33:
                    color = self.colors['low_progress']
                elif progress < 66:
                    color = self.colors['med_progress']
                else:
                    color = self.colors['high_progress']

                # Draw progress bar
                bar_width = bar_bg.winfo_reqwidth()
                bar_bg.create_rectangle(
                    0, 0,
                    (progress / 100) * bar_width, 20,
                    fill=color,
                    width=0
                )

                # Progress percentage
                progress_label = ttk.Label(
                    task_frame,
                    text=f"{progress}%",
                    style="DashboardProgress.TLabel",
                    foreground=color
                )
                progress_label.pack(anchor="e")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()