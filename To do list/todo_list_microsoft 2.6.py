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
            'primary': '#2196F3',
            'secondary': '#FFC107',
            'background': '#FFFFFF',
            'surface': '#F5F5F5',
            'text': '#212121',
            'border': '#E0E0E0'
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
            foreground='white',
            font=('Segoe UI', 11, 'bold'),
            padding=8
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
        
    def create_task_grid(self):
        grid_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        grid_frame.pack(fill="both", expand=True)
        
        # Days of week headers
        days = ["Task", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days):
            label = ttk.Label(
                grid_frame,
                text=day,
                style="Day.TLabel"
            )
            label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
        
        # Task rows
        for row in range(1, 16):
            # Task description
            task_entry = ttk.Entry(
                grid_frame,
                font=('Segoe UI', 10)
            )
            task_entry.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
            
            # Checkboxes for each day
            for day in range(1, 8):
                var = tk.BooleanVar()
                check = ttk.Checkbutton(
                    grid_frame,
                    variable=var,
                    style="Tracker.TCheckbutton"
                )
                check.grid(row=row, column=day, sticky="nsew", padx=1, pady=1)
        
        # Configure grid weights
        grid_frame.grid_columnconfigure(0, weight=2)  # Task column wider
        for i in range(1, 8):
            grid_frame.grid_columnconfigure(i, weight=1)
            
    def create_goals_section(self):
        goals_frame = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        goals_frame.pack(fill="x", pady=20)
        
        # Goals section
        goals_label = ttk.Label(
            goals_frame,
            text="Weekly Goals",
            style="Header.TLabel"
        )
        goals_label.pack(anchor="w", pady=(0, 10))
        
        self.goals_text = tk.Text(
            goals_frame,
            height=4,
            font=('Segoe UI', 10),
            wrap="word"
        )
        self.goals_text.pack(fill="x")
        
        # Rewards section
        rewards_label = ttk.Label(
            goals_frame,
            text="Rewards",
            style="Header.TLabel"
        )
        rewards_label.pack(anchor="w", pady=(20, 10))
        
        self.rewards_text = tk.Text(
            goals_frame,
            height=4,
            font=('Segoe UI', 10),
            wrap="word"
        )
        self.rewards_text.pack(fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()