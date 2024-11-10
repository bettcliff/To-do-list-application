import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class WeeklyTaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Task Tracker")
        self.root.geometry("1000x800")
        
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
            'progress': '#4CAF50'       # Green for progress
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
        
    def create_layout(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header()
        
        # Task grid
        self.create_task_grid()
        
        # Goals and rewards section
        self.create_goals_section()
        
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Current month and week
        current_date = datetime.now()
        month = current_date.strftime("%B %Y")
        week_num = (current_date.day - 1) // 7 + 1
        
        month_label = ttk.Label(
            header_frame,
            text=f"Month: {month}",
            style="Header.TLabel"
        )
        month_label.pack(side="left", padx=10)
        
        week_label = ttk.Label(
            header_frame,
            text=f"Week {week_num}",
            style="Header.TLabel"
        )
        week_label.pack(side="left", padx=10)

        # Add overall progress label
        self.overall_progress_label = ttk.Label(
            header_frame,
            text="Overall Progress: 0%",
            style="Header.TLabel"
        )
        self.overall_progress_label.pack(side="right", padx=10)
        
    def create_task_grid(self):
        grid_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        grid_frame.pack(fill="both", expand=True)
        
        # Days of week headers
        days = ["Task", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Progress"]
        for i, day in enumerate(days):
            label = ttk.Label(
                grid_frame,
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
                grid_frame,
                font=('Segoe UI', 10),
                style='Task.TEntry'
            )
            task_entry.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Checkboxes for each day
            row_vars = []
            for day in range(1, 8):
                var = tk.BooleanVar()
                var.trace('w', lambda *args, r=row: self.update_all_progress(r))
                check = ttk.Checkbutton(
                    grid_frame,
                    variable=var,
                    style="Tracker.TCheckbutton"
                )
                check.grid(row=row, column=day, sticky="nsew", padx=1, pady=1)
                row_vars.append(var)
            self.task_vars.append(row_vars)
            
            # Progress label
            progress_label = ttk.Label(
                grid_frame,
                text="0%",
                style="Progress.TLabel"
            )
            progress_label.grid(row=row, column=8, sticky="nsew", padx=1, pady=1)
            self.progress_labels.append(progress_label)
        
        # Configure grid weights
        grid_frame.grid_columnconfigure(0, weight=2)  # Task column wider
        for i in range(1, 9):
            grid_frame.grid_columnconfigure(i, weight=1)
            
    def update_all_progress(self, row):
        # Update individual task progress
        checked_count = sum(1 for var in self.task_vars[row-1] if var.get())
        percentage = int((checked_count / 7) * 100)
        self.progress_labels[row-1].configure(text=f"{percentage}%")
        
        # Update overall progress
        total_tasks = len(self.task_vars) * 7  # Total possible checkboxes
        total_checked = sum(sum(1 for var in row if var.get()) for row in self.task_vars)
        overall_percentage = int((total_checked / total_tasks) * 100)
        self.overall_progress_label.configure(text=f"Overall Progress: {overall_percentage}%")
            
    def create_goals_section(self):
        goals_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        goals_frame.pack(fill="x", pady=20)

        # Create a frame to hold goals and rewards side by side
        content_frame = ttk.Frame(goals_frame, style="Tracker.TFrame")
        content_frame.pack(fill="x")
        
        # Goals section - Left side
        goals_container = ttk.Frame(content_frame, style="Tracker.TFrame")
        goals_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        goals_label = ttk.Label(
            goals_container,
            text="Weekly Goals",
            style="Header.TLabel"
        )
        goals_label.pack(anchor="w", pady=(0, 10))
        
        self.goals_text = tk.Text(
            goals_container,
            height=4,
            font=('Segoe UI', 10),
            wrap="word",
            bg=self.colors['surface'],
            fg=self.colors['text']
        )
        self.goals_text.pack(fill="x")
        
        # Rewards section - Right side
        rewards_container = ttk.Frame(content_frame, style="Tracker.TFrame")
        rewards_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        rewards_label = ttk.Label(
            rewards_container,
            text="Rewards for Completion",
            style="Header.TLabel"
        )
        rewards_label.pack(anchor="w", pady=(0, 10))
        
        self.rewards_text = tk.Text(
            rewards_container,
            height=4,
            font=('Segoe UI', 10),
            wrap="word",
            bg=self.colors['surface'],
            fg=self.colors['text']
        )
        self.rewards_text.pack(fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()