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
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create pages
        self.tasks_page = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        self.progress_page = ttk.Frame(self.main_frame, style="Tracker.TFrame")
        
        # Tasks page layout
        self.tracker_frame = ttk.Frame(self.tasks_page, style="Tracker.TFrame")
        self.tracker_frame.pack(side="left", fill="both", expand=True)
        
        self.right_frame = ttk.Frame(self.tasks_page, style="Tracker.TFrame")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        # History section
        self.history_frame = ttk.Frame(self.right_frame, style="Tracker.TFrame")
        self.history_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Create components
        self.create_dashboard()
        self.create_history_section()
        self.create_header()
        self.create_task_grid()
        self.create_goals_section()
        
        # Show tasks page by default
        self.show_tasks_page()
        
    def show_tasks_page(self):
        self.progress_page.pack_forget()
        self.tasks_page.pack(fill="both", expand=True)
        
    def show_progress_page(self):
        self.tasks_page.pack_forget()
        self.progress_page.pack(fill="both", expand=True)
        self.update_dashboard()

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
        
        # Update dashboard if progress page is visible
        if self.progress_page.winfo_ismapped():
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

        # Add task count label
        self.task_count_label = ttk.Label(
            header_frame,
            text="Tasks: 0",
            style="Header.TLabel"
        )
        self.task_count_label.pack(side="left", padx=10)

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

    def add_task_row(self):
        row = len(self.task_vars) + 1
        
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
        
        return task_entry

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
            # Create new task row
            new_task_entry = self.add_task_row()
            new_task_entry.insert(0, f"Task {self.task_count + 1}: {task_text}")
            
            # Store task name
            self.task_names.append(task_text)
            
            # Increment task count and update label
            self.task_count += 1
            self.task_count_label.configure(text=f"Tasks: {self.task_count}")
            
            # Clear entries
            task_entry.delete(0, 'end')
            task_entry.insert(0, "Enter task...")
            reward_entry.delete(0, 'end')
            reward_entry.insert(0, "Enter reward...")

    def create_dashboard(self):
        # Create figure for matplotlib
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(6, 12),
                                                      facecolor=self.colors['chart_bg'])
        
        # Configure progress chart
        self.ax1.set_facecolor(self.colors['chart_bg'])
        self.ax1.set_title('Task Progress', color=self.colors['text'])
        self.ax1.tick_params(colors=self.colors['text'])
        
        # Configure completion trend chart
        self.ax2.set_facecolor(self.colors['chart_bg'])
        self.ax2.set_title('Daily Completion Trend', color=self.colors['text'])
        self.ax2.tick_params(colors=self.colors['text'])
        
        # Configure pie chart
        self.ax3.set_facecolor(self.colors['chart_bg'])
        self.ax3.set_title('Task Distribution', color=self.colors['text'])
        
        # Embed charts in progress page
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.progress_page)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def update_dashboard(self):
        # Clear previous charts
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
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
        
        # Update pie chart
        if task_names:  # Only create pie chart if there are tasks
            colors = plt.cm.Set3(np.linspace(0, 1, len(progress)))
            self.ax3.pie(progress, labels=task_names, colors=colors, autopct='%1.1f%%',
                        textprops={'color': self.colors['text']})
            self.ax3.set_title('Task Distribution', color=self.colors['text'])
        
        # Refresh canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()