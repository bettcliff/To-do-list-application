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
        self.root.geometry("1000x800")
        
        # Initialize tasks
        self.tasks = self.load_tasks()
        
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

        style.configure(
            "Dashboard.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text']
        )
        
    def create_layout(self):
        """Create main layout"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create dashboard
        self.create_dashboard(self.main_frame)  # Pass main_frame as parent

    def create_dashboard(self, parent):
        """Create the analytics dashboard with pie chart"""
        # Title
        title = ttk.Label(
            parent,  # Use parent instead of self
            text="Task Analytics Dashboard",
            font=("Segoe UI", 24, "bold"),
            style="Dashboard.TLabel"
        )
        title.pack(pady=20)
        
        # Create graphs container
        graphs_frame = ttk.Frame(parent)  # Use parent
        graphs_frame.pack(fill="both", expand=True, padx=20)
        
        # Create pie chart
        self.create_pie_chart(graphs_frame)
        
        # Create summary section
        self.create_summary_section(parent)  # Pass parent

    def create_summary_section(self, parent):
        """Create summary statistics section"""
        summary_frame = ttk.Frame(parent)  # Use parent instead of self
        summary_frame.pack(fill="x", padx=20, pady=20)
        
        # Calculate statistics
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks 
                             if task.get("status") == "Completed")
        
        # Avoid division by zero
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Today's tasks
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = sum(1 for task in self.tasks 
                         if task.get("due_date") == today)
        
        # Create summary cards
        summaries = [
            {
                "title": "Total Tasks",
                "value": str(total_tasks),
                "color": "#2196F3"
            },
            {
                "title": "Completed",
                "value": f"{completed_tasks} ({completion_rate:.1f}%)",
                "color": "#4CAF50"
            },
            {
                "title": "Due Today",
                "value": str(today_tasks),
                "color": "#FFC107"
            }
        ]
        
        # Create and style cards
        for summary in summaries:
            card = ttk.Frame(
                summary_frame,
                style="Card.TFrame"
            )
            card.pack(side="left", padx=10, expand=True, fill="both")
            
            # Title
            ttk.Label(
                card,
                text=summary["title"],
                font=("Segoe UI", 12),
                foreground=summary["color"],
                style="Card.TLabel"
            ).pack(pady=(10, 5))
            
            # Value
            ttk.Label(
                card,
                text=summary["value"],
                font=("Segoe UI", 24, "bold"),
                style="Card.TLabel"
            ).pack(pady=(0, 10))

    def create_pie_chart(self, parent):
        """Create pie chart for task status"""
        # Calculate statistics
        total_tasks = len(self.tasks)
        
        # Handle empty task list
        if total_tasks == 0:
            # Create empty chart with message
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('#F5F5F5')
            
            # Display "No Data" message on both charts
            for ax in [ax1, ax2]:
                ax.text(0.5, 0.5, 'No tasks available',
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=ax.transAxes,
                       fontsize=12)
                ax.axis('off')
        else:
            # Calculate task statistics
            completed = sum(1 for task in self.tasks 
                           if task.get("status") == "Completed")
            pending = total_tasks - completed
            
            # Create figure
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('#F5F5F5')
            
            # Status Pie Chart (Left)
            if completed == 0 and pending == 0:
                # Handle case where all values are 0
                status_sizes = [1]
                status_labels = ['No Tasks']
                status_colors = ['#E0E0E0']
                explode = None
            else:
                status_sizes = [completed, pending]
                status_labels = ['Completed', 'Pending']
                status_colors = ['#4CAF50', '#FFC107']
                explode = (0.05, 0)
            
            ax1.pie(status_sizes, 
                    labels=status_labels, 
                    colors=status_colors,
                    autopct='%1.1f%%' if sum(status_sizes) > 0 else None,
                    startangle=90,
                    explode=explode)
            ax1.set_title('Task Completion Status', pad=20)
            
            # Category Pie Chart (Right)
            categories = ["My Day", "Important", "Planned", "Personal", "Work", "Shopping"]
            category_counts = []
            category_colors = ['#2196F3', '#F44336', '#4CAF50', '#9C27B0', '#FF9800', '#00BCD4']
            
            # Count tasks in each category
            for category in categories:
                count = sum(1 for task in self.tasks 
                           if task.get("category") == category)
                category_counts.append(count)
            
            # Handle case where all categories are empty
            if sum(category_counts) == 0:
                category_counts = [1]
                categories = ['No Tasks']
                category_colors = ['#E0E0E0']
            
            ax2.pie(category_counts, 
                    labels=categories, 
                    colors=category_colors,
                    autopct='%1.1f%%' if sum(category_counts) > 0 else None,
                    startangle=90)
            ax2.set_title('Tasks by Category', pad=20)
        
        # Adjust layout
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

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

    def update_dashboard(self):
        """Refresh the dashboard data"""
        # Clear existing widgets in dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
            
        # Recreate dashboard
        self.create_dashboard()

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                # Ensure all tasks have required fields
                for task in tasks:
                    if "category" not in task:
                        task["category"] = "My Day"
                    if "status" not in task:
                        task["status"] = "Pending"
                return tasks
        except FileNotFoundError:
            # Return empty list if file doesn't exist
            return []
        except json.JSONDecodeError:
            # Handle corrupted file
            print("Warning: Tasks file is corrupted. Starting with empty task list.")
            return []
        except Exception as e:
            # Handle other errors
            print(f"Error loading tasks: {str(e)}")
            return []
            
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {str(e)}")
            
    def add_task(self, task_text, category="My Day"):
        """Add a new task"""
        if task_text.strip():
            task = {
                "task": task_text,
                "category": category,
                "status": "Pending",
                "due_date": datetime.now().strftime("%Y-%m-%d"),
                "priority": "Normal"
            }
            self.tasks.append(task)
            self.save_tasks()
            
    def complete_task(self, task_index):
        """Mark a task as completed"""
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]["status"] = "Completed"
            self.save_tasks()
            
    def delete_task(self, task_index):
        """Delete a task"""
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()