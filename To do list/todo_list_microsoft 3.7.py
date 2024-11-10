import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime

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
        
        # Create components
        self.create_dashboard()
        self.create_history_section()
        self.create_header()
        self.create_goals_section() # Moved up before task grid
        self.create_task_grid()

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
        
        for i, row_vars in enumerate(self.task_vars):
            task_text = self.grid_frame.grid_slaves(row=i+1, column=0)[0].get()
            task_progress = float(self.progress_labels[i].cget("text").strip('%'))
            week_data['tasks'].append({
                'description': task_text,
                'progress': task_progress,
                'daily_completion': [var.get() for var in row_vars]
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

    def update_progress(self, row):
        # Update individual task progress
        checked_count = sum(1 for var in self.task_vars[row-1] if var.get())
        percentage = int((checked_count / 7) * 100)
        self.progress_labels[row-1].configure(text=f"{percentage}%")
        
        # Update overall progress
        total_tasks = len(self.task_vars) * 7  # Total possible checkboxes
        total_checked = sum(sum(1 for var in row if var.get()) for row in self.task_vars)
        overall_percentage = int((total_checked / total_tasks) * 100)
        self.overall_progress_label.configure(text=f"Overall Progress: {overall_percentage}%")
        
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

        # Add initial task-reward pair
        self.add_task_reward_pair()

        # Add button for new task-reward pairs
        add_pair_button = ttk.Button(
            rewards_frame,
            text="Add Task-Reward Pair",
            command=self.add_task_reward_pair
        )
        add_pair_button.pack(pady=(10, 0))

    def add_task_reward_pair(self):
        pair_frame = ttk.Frame(self.reward_pairs_frame, style="Tracker.TFrame")
        pair_frame.pack(fill="x", pady=5)

        # Find first empty task row
        empty_row = None
        for i, row in enumerate(range(1, 16)):
            task_entry = self.grid_frame.grid_slaves(row=row, column=0)[0]
            if not task_entry.get():
                empty_row = i
                break

        if empty_row is not None:
            task_entry = ttk.Entry(
                pair_frame,
                font=('Segoe UI', 10),
                width=30
            )
            task_entry.insert(0, "Enter task...")
            task_entry.bind('<FocusIn>', lambda e: self.on_task_focus_in(e, task_entry, empty_row))
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

    def on_task_focus_in(self, event, task_entry, row):
        if task_entry.get() == "Enter task...":
            task_entry.delete(0, 'end')
        
        # When task is entered, copy it to the main task grid
        def on_task_change(*args):
            main_task_entry = self.grid_frame.grid_slaves(row=row+1, column=0)[0]
            main_task_entry.delete(0, 'end')
            main_task_entry.insert(0, task_entry.get())
        
        task_entry.bind('<KeyRelease>', on_task_change)

    def create_dashboard(self):
        # Create figure for matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8),
                                                      facecolor=self.colors['chart_bg'])
        
        # Configure progress chart
        self.ax1.set_facecolor(self.colors['chart_bg'])
        self.ax1.set_title('Task Progress', color=self.colors['text'])
        self.ax1.tick_params(colors=self.colors['text'])
        
        # Configure completion trend chart
        self.ax2.set_facecolor(self.colors['chart_bg'])
        self.ax2.set_title('Daily Completion Trend', color=self.colors['text'])
        self.ax2.tick_params(colors=self.colors['text'])
        
        # Embed charts in dashboard frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.dashboard_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def update_dashboard(self):
        # Clear previous charts
        self.ax1.clear()
        self.ax2.clear()
        
        # Update progress chart
        task_names = []
        progress = []
        for i, row_vars in enumerate(self.task_vars):
            task_text = self.grid_frame.grid_slaves(row=i+1, column=0)[0].get()
            if task_text:  # Only show tasks with descriptions
                task_names.append(task_text)
                checked = sum(1 for var in row_vars if var.get())
                progress.append((checked / 7) * 100)
        
        if task_names:  # Only create chart if there are tasks
            self.ax1.barh(task_names, progress, color=self.colors['primary'])
            self.ax1.set_title('Task Progress', color=self.colors['text'])
            self.ax1.set_xlabel('Completion %', color=self.colors['text'])
        
        # Update trend chart
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_completion = []
        for day in range(7):
            tasks_with_description = sum(1 for i, row in enumerate(self.task_vars) 
                                       if self.grid_frame.grid_slaves(row=i+1, column=0)[0].get())
            if tasks_with_description > 0:
                completed = sum(1 for i, row in enumerate(self.task_vars) 
                              if row[day].get() and self.grid_frame.grid_slaves(row=i+1, column=0)[0].get())
                daily_completion.append((completed / tasks_with_description) * 100)
            else:
                daily_completion.append(0)
        
        self.ax2.plot(days, daily_completion, color=self.colors['primary'],
                     marker='o', linewidth=2)
        self.ax2.set_title('Daily Completion Trend', color=self.colors['text'])
        self.ax2.set_ylabel('Completion %', color=self.colors['text'])
        
        # Refresh canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()