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
        
        # Initialize tasks and history
        self.tasks = self.load_tasks()
        self.task_history = []
        self.load_task_history()
        
        # Apply modern styles
        self.apply_styles()
        
        # Create main layout
        self.create_layout()
        
        # Create task details window
        self.task_details_window = None
        
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

        style.configure(
            "Task.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
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

    def show_task_details(self, row):
        # Destroy existing window if open
        if self.task_details_window and self.task_details_window.winfo_exists():
            self.task_details_window.destroy()
            
        # Create new window
        self.task_details_window = tk.Toplevel(self.root)
        self.task_details_window.title("Task Details")
        self.task_details_window.geometry("600x400")
        self.task_details_window.configure(bg=self.colors['background'])
        
        # Get task info
        task_entry = self.grid_frame.grid_slaves(row=row, column=0)[0]
        task_name = task_entry.get()
        
        # Task name header
        ttk.Label(
            self.task_details_window,
            text=f"Task: {task_name}",
            style="Header.TLabel"
        ).pack(fill="x", pady=10)
        
        # Create figure for task details chart
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=self.colors['chart_bg'])
        ax.set_facecolor(self.colors['chart_bg'])
        
        # Plot daily completion status
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        completion = [1 if var.get() else 0 for var in self.task_vars[row-1]]
        
        ax.bar(days, completion, color=self.colors['primary'])
        ax.set_title('Weekly Task Completion', color=self.colors['text'])
        ax.set_ylabel('Completed', color=self.colors['text'])
        ax.tick_params(colors=self.colors['text'])
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.task_details_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add task statistics
        stats_frame = ttk.Frame(self.task_details_window, style="Tracker.TFrame")
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        completed_days = sum(1 for var in self.task_vars[row-1] if var.get())
        completion_rate = (completed_days / 7) * 100
        
        ttk.Label(
            stats_frame,
            text=f"Days Completed: {completed_days}/7",
            style="History.TLabel"
        ).pack(side="left", padx=10)
        
        ttk.Label(
            stats_frame,
            text=f"Completion Rate: {completion_rate:.1f}%",
            style="History.TLabel"
        ).pack(side="left", padx=10)

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
            # Task description as clickable label
            task_label = ttk.Label(
                self.grid_frame,
                text="",
                style='Task.TLabel'
            )
            task_label.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            task_label.bind('<Button-1>', lambda e, r=row: self.show_task_details(r))
            
            # Entry for editing task name
            task_entry = ttk.Entry(
                self.grid_frame,
                font=('Segoe UI', 10)
            )
            task_entry.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            task_entry.bind('<FocusOut>', lambda e, r=row: self.update_task_label(r))
            
            # Checkboxes for each day
            row_vars = []
            for col in range(1, 8):
                var = tk.BooleanVar()
                checkbox = ttk.Checkbutton(
                    self.grid_frame,
                    variable=var,
                    command=lambda r=row: self.update_progress(r)
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

    def update_task_label(self, row):
        task_entry = self.grid_frame.grid_slaves(row=row, column=0)[1]  # Get entry widget
        task_label = self.grid_frame.grid_slaves(row=row, column=0)[0]  # Get label widget
        task_label.configure(text=task_entry.get())

    def load_task_history(self):
        """Load task completion history from file"""
        try:
            with open("task_history.json", "r") as file:
                self.task_history = json.load(file)
        except FileNotFoundError:
            self.task_history = []
        except json.JSONDecodeError:
            print("Warning: Task history file is corrupted. Starting with empty history.")
            self.task_history = []
        except Exception as e:
            print(f"Error loading task history: {str(e)}")
            self.task_history = []
            
    def save_task_history(self):
        """Save task completion history to file"""
        try:
            with open("task_history.json", "w") as file:
                json.dump(self.task_history, file, indent=4)
        except Exception as e:
            print(f"Error saving task history: {str(e)}")
            
    def add_to_history(self, task):
        """Add completed task to history"""
        history_entry = {
            "task": task["task"],
            "category": task["category"],
            "completed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": task.get("due_date", ""),
            "priority": task.get("priority", "Normal")
        }
        self.task_history.append(history_entry)
        self.save_task_history()
        
    def complete_task(self, task_index):
        """Mark a task as completed and add to history"""
        if 0 <= task_index < len(self.tasks):
            task = self.tasks[task_index]
            task["status"] = "Completed"
            task["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to history
            self.add_to_history(task)
            
            # Save changes
            self.save_tasks()
            
    def get_completion_stats(self):
        """Get task completion statistics"""
        if not self.task_history:
            return {
                "total_completed": 0,
                "avg_completion_time": 0,
                "completion_by_category": {},
                "completion_by_priority": {}
            }
            
        stats = {
            "total_completed": len(self.task_history),
            "completion_by_category": {},
            "completion_by_priority": {}
        }
        
        # Calculate completion by category
        for entry in self.task_history:
            category = entry.get("category", "Uncategorized")
            priority = entry.get("priority", "Normal")
            
            stats["completion_by_category"][category] = \
                stats["completion_by_category"].get(category, 0) + 1
            stats["completion_by_priority"][priority] = \
                stats["completion_by_priority"].get(priority, 0) + 1
            
        return stats
        
    def get_recent_completions(self, days=7):
        """Get recently completed tasks"""
        if not self.task_history:
            return []
            
        current_date = datetime.now()
        recent_tasks = []
        
        for entry in self.task_history:
            completed_date = datetime.strptime(
                entry["completed_date"],
                "%Y-%m-%d %H:%M:%S"
            )
            if (current_date - completed_date).days <= days:
                recent_tasks.append(entry)
                
        return recent_tasks

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()