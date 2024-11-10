import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WeeklyTaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly Task Tracker")
        self.root.geometry("1000x800")
        
        # Initialize data structures first
        self.tasks = []
        self.task_history = []
        
        # Initialize tasks
        self.load_tasks()
        self.load_task_history()
        
        # Apply modern styles
        self.apply_styles()
        
        # Create main layout
        self.create_layout()
        
        # Create task details window
        self.task_details_window = None
        
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
                # Ensure all tasks have required fields
                for task in self.tasks:
                    if "category" not in task:
                        task["category"] = "My Day"
                    if "status" not in task:
                        task["status"] = "Pending"
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Warning: Tasks file is corrupted. Starting with empty task list.")
            self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {str(e)}")
            self.tasks = []

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

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {str(e)}")

    def save_task_history(self):
        """Save task completion history to file"""
        try:
            with open("task_history.json", "w") as file:
                json.dump(self.task_history, file, indent=4)
        except Exception as e:
            print(f"Error saving task history: {str(e)}")

    def apply_styles(self):
        """Apply modern styles to the application"""
        style = ttk.Style()
        
        # Color scheme
        self.colors = {
            'primary': '#2196F3',      # Blue
            'secondary': '#FFC107',    # Amber
            'success': '#4CAF50',      # Green
            'danger': '#F44336',       # Red
            'background': '#F5F5F5',   # Light Gray
            'surface': '#FFFFFF',      # White
            'text': '#212121',         # Dark Gray
            'text_secondary': '#757575' # Medium Gray
        }
        
        # Configure styles
        style.configure(
            "Tracker.TFrame",
            background=self.colors['background']
        )
        
        style.configure(
            "Card.TFrame",
            background=self.colors['surface']
        )
        
        style.configure(
            "Dashboard.TLabel",
            background=self.colors['background'],
            foreground=self.colors['text']
        )
        
        style.configure(
            "Card.TLabel",
            background=self.colors['surface'],
            foreground=self.colors['text']
        )

    def create_layout(self):
        """Create main layout"""
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Tracker.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create dashboard
        self.create_dashboard(self.main_frame)

    def create_dashboard(self, parent):
        """Create the analytics dashboard"""
        # Title
        title = ttk.Label(
            parent,
            text="Task Analytics Dashboard",
            font=("Segoe UI", 24, "bold"),
            style="Dashboard.TLabel"
        )
        title.pack(pady=20)
        
        # Create graphs container
        graphs_frame = ttk.Frame(parent)
        graphs_frame.pack(fill="both", expand=True, padx=20)
        
        # Create pie chart
        self.create_pie_chart(graphs_frame)
        
        # Create summary section
        self.create_summary_section(parent)

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
            task = self.tasks[task_index]
            task["status"] = "Completed"
            task["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to history
            self.add_to_history(task)
            
            # Save changes
            self.save_tasks()

    def delete_task(self, task_index):
        """Delete a task"""
        if 0 <= task_index < len(self.tasks):
            self.tasks.pop(task_index)
            self.save_tasks()

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

    def create_summary_section(self, parent):
        """Create summary statistics section with history"""
        summary_frame = ttk.Frame(parent)
        summary_frame.pack(fill="x", padx=20, pady=20)
        
        # Get stats
        stats = self.get_completion_stats()
        recent = len(self.get_recent_completions(7))
        
        # Create summary cards
        summaries = [
            {
                "title": "Total Tasks",
                "value": str(len(self.tasks)),
                "color": "#2196F3"
            },
            {
                "title": "All Time Completed",
                "value": str(stats["total_completed"]),
                "color": "#4CAF50"
            },
            {
                "title": "Completed (7 days)",
                "value": str(recent),
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

if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTaskTracker(root)
    root.mainloop()