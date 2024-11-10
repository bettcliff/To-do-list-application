import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ModernToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Task Manager")
        self.root.geometry("1200x800")
        
        # Initialize tasks list
        self.tasks = self.load_tasks()
        self.current_category = "My Day"
        
        # Create main layout first
        self.create_main_layout()
        
        # Apply modern styles after task_tree is created
        self.apply_modern_styles()
        
    def apply_modern_styles(self):
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
            "Modern.TFrame",
            background=self.colors['background']
        )
        
        style.configure(
            "Modern.TButton",
            padding=10,
            background=self.colors['primary'],
            foreground=self.colors['surface'],
            font=('Segoe UI', 10)
        )
        
        style.configure(
            "Modern.TLabel",
            background=self.colors['background'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10),
            padding=5
        )
        
        style.configure(
            "Header.TLabel",
            font=('Segoe UI', 24, 'bold'),
            foreground=self.colors['primary']
        )
        
        # Add styles for completed tasks
        style.configure(
            "Modern.Treeview",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            fieldbackground=self.colors['surface'],
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        
        # Configure tag styles
        if hasattr(self, 'task_tree'):
            self.task_tree.tag_configure(
                "completed",
                foreground=self.colors['text_secondary'],
                font=('Segoe UI', 10, 'overstrike')
            )
            
            self.task_tree.tag_configure(
                "pending",
                foreground=self.colors['text'],
                font=('Segoe UI', 10)
            )
        
    def create_main_layout(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, style="Modern.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        self.content_frame.pack(fill="both", expand=True, pady=20)
        
        # Create task input and list
        self.create_task_input()
        self.create_task_list()
        
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style="Modern.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title = ttk.Label(
            header_frame,
            text="Task Manager",
            style="Header.TLabel"
        )
        title.pack(side="left")
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="Modern.TFrame")
        nav_frame.pack(side="right")
        
        categories = ["My Day", "Important", "Tasks", "Completed"]
        for category in categories:
            btn = ttk.Button(
                nav_frame,
                text=category,
                style="Modern.TButton",
                command=lambda c=category: self.switch_category(c)
            )
            btn.pack(side="left", padx=5)
            
    def create_task_input(self):
        input_frame = ttk.Frame(self.content_frame, style="Modern.TFrame")
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Task entry
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=('Segoe UI', 12),
            width=40
        )
        task_entry.pack(side="left", padx=(0, 10))
        
        # Add button
        add_btn = ttk.Button(
            input_frame,
            text="Add Task",
            style="Modern.TButton",
            command=self.add_task
        )
        add_btn.pack(side="left")
        
    def create_task_list(self):
        # Create frame for task list
        list_frame = ttk.Frame(self.content_frame, style="Modern.TFrame")
        list_frame.pack(fill="both", expand=True)
        
        # Create Treeview for tasks
        columns = ("Completed", "Task", "Due Date", "Priority", "Status")
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            style="Modern.Treeview"
        )
        
        # Configure columns
        self.task_tree.heading("Completed", text="✓")
        self.task_tree.column("Completed", width=50, anchor="center")
        
        for col in columns[1:]:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.task_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind events
        self.task_tree.bind("<Button-1>", self.on_click)
        self.task_tree.bind("<Button-3>", self.show_task_menu)
        
    def on_click(self, event):
        """Handle click events on the task list"""
        region = self.task_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.task_tree.identify_column(event.x)
            if column == "#1":  # Completed column
                item = self.task_tree.identify_row(event.y)
                if item:
                    self.toggle_task_completion(item)
                    
    def toggle_task_completion(self, item):
        """Toggle task completion status"""
        values = self.task_tree.item(item)['values']
        task_text = values[1]  # Task is in second column
        
        # Find and update task in tasks list
        for task in self.tasks:
            if task["task"] == task_text:
                task["status"] = "Completed" if task["status"] != "Completed" else "Pending"
                self.save_tasks()
                self.refresh_task_list()
                break
                
    def refresh_task_list(self):
        """Refresh the task list display"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # Sort tasks: pending first, then completed
        pending_tasks = []
        completed_tasks = []
        
        for task in self.tasks:
            if task["category"] == self.current_category:
                if task["status"] == "Completed":
                    completed_tasks.append(task)
                else:
                    pending_tasks.append(task)
        
        # Add pending tasks
        for task in pending_tasks:
            check = "☐"
            values = (
                check,
                task["task"],
                task["due_date"],
                task["priority"],
                task["status"]
            )
            self.task_tree.insert("", "end", values=values, tags=("pending",))
        
        # Add completed tasks
        for task in completed_tasks:
            check = "☑"
            values = (
                check,
                task["task"],
                task["due_date"],
                task["priority"],
                task["status"]
            )
            self.task_tree.insert("", "end", values=values, tags=("completed",))
            
        # Update task counter
        total = len(pending_tasks) + len(completed_tasks)
        completed = len(completed_tasks)
        self.update_task_counter(total, completed)
        
    def update_task_counter(self, total, completed):
        """Update the task counter display"""
        if hasattr(self, 'counter_label'):
            self.counter_label.config(
                text=f"Completed: {completed}/{total} ({int(completed/total*100) if total > 0 else 0}%)"
            )
            
    def switch_category(self, category):
        self.current_category = category
        self.refresh_task_list()
        
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            new_task = {
                "task": task,
                "due_date": datetime.now().strftime("%Y-%m-%d"),
                "priority": "Normal",
                "category": self.current_category,
                "status": "Pending"
            }
            
            self.tasks.append(new_task)
            self.save_tasks()
            self.refresh_task_list()
            self.task_var.set("")
            
    def show_task_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Complete", command=self.complete_task)
        menu.add_command(label="Delete", command=self.delete_task)
        menu.tk_popup(event.x_root, event.y_root)
        
    def complete_task(self):
        selected = self.task_tree.selection()
        if selected:
            item = selected[0]
            task_idx = self.task_tree.index(item)
            self.tasks[task_idx]["status"] = "Completed"
            self.save_tasks()
            self.refresh_task_list()
            
    def delete_task(self):
        selected = self.task_tree.selection()
        if selected:
            if messagebox.askyesno("Confirm", "Delete this task?"):
                item = selected[0]
                task_idx = self.task_tree.index(item)
                self.tasks.pop(task_idx)
                self.save_tasks()
                self.refresh_task_list()
                
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
            
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernToDoList(root)
    root.mainloop()