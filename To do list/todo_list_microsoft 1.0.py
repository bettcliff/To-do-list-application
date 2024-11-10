import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
import os
from PIL import Image, ImageTk

class ModernToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Microsoft To Do")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F5F5F5")
        
        # Load data
        self.tasks = self.load_tasks()
        self.categories = ["My Day", "Important", "Planned", "Personal", "Work", "Shopping"]
        self.current_category = "My Day"
        
        # Create main container with grid
        self.setup_grid()
        self.create_widgets()
        self.apply_styles()
        
    def setup_grid(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
    def apply_styles(self):
        style = ttk.Style()
        
        # Configure modern styles
        style.configure("Sidebar.TFrame", background="#F0F0F0")
        style.configure("Content.TFrame", background="#FFFFFF")
        style.configure("Category.TButton", 
                       font=("Segoe UI", 11),
                       padding=10,
                       background="#F0F0F0")
        style.configure("Task.TCheckbutton",
                       font=("Segoe UI", 11),
                       background="#FFFFFF")
        
    def create_widgets(self):
        self.create_sidebar()
        self.create_content_area()
        
    def create_sidebar(self):
        # Sidebar container
        sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", padding="10")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # User profile section
        profile_frame = ttk.Frame(sidebar)
        profile_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(
            profile_frame,
            text="📝 Microsoft To Do",
            font=("Segoe UI", 16, "bold"),
            background="#F0F0F0"
        ).pack(pady=10)
        
        # Category buttons
        for category in self.categories:
            self.create_category_button(sidebar, category)
            
    def create_category_button(self, parent, category):
        icon_map = {
            "My Day": "☀️",
            "Important": "⭐",
            "Planned": "📅",
            "Personal": "👤",
            "Work": "💼",
            "Shopping": "🛒"
        }
        
        # Create a frame for each button to handle highlighting
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=2)
        
        btn = ttk.Button(
            btn_frame,
            text=f"{icon_map.get(category, '📌')} {category}",
            style="Category.TButton",
            command=lambda c=category: self.switch_category(c)
        )
        btn.pack(fill="x")
        
        # Store button reference for highlighting
        if not hasattr(self, 'category_buttons'):
            self.category_buttons = {}
        self.category_buttons[category] = btn
        
    def create_content_area(self):
        # Main content area
        content = ttk.Frame(self.root, style="Content.TFrame", padding="20")
        content.grid(row=0, column=1, sticky="nsew")
        
        # Header
        header = ttk.Frame(content)
        header.pack(fill="x", pady=(0, 20))
        
        self.category_label = ttk.Label(
            header,
            text=self.current_category,
            font=("Segoe UI", 24, "bold"),
            background="#FFFFFF"
        )
        self.category_label.pack(side="left")
        
        # Task input area
        input_frame = ttk.Frame(content)
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Task entry
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=("Segoe UI", 12),
            width=40
        )
        task_entry.pack(side="left", padx=(0, 10))
        
        # Due date picker
        self.due_date = DateEntry(
            input_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2
        )
        self.due_date.pack(side="left", padx=5)
        
        # Priority selector
        self.priority_var = tk.StringVar(value="Normal")
        priority_frame = ttk.Frame(input_frame)
        priority_frame.pack(side="left", padx=5)
        
        priorities = ["Low", "Normal", "High"]
        priority_menu = ttk.OptionMenu(
            priority_frame,
            self.priority_var,
            "Normal",
            *priorities
        )
        priority_menu.pack(side="left")
        
        # Add task button
        add_btn = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            style="Accent.TButton"
        )
        add_btn.pack(side="left", padx=5)
        
        # Tasks list
        self.create_tasks_list(content)
        
    def create_tasks_list(self, parent):
        # Tasks container
        tasks_frame = ttk.Frame(parent)
        tasks_frame.pack(fill="both", expand=True)
        
        # Treeview for tasks
        columns = ("Task", "Due Date", "Priority", "Category", "Status")
        self.task_tree = ttk.Treeview(
            tasks_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=150)
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tasks_frame,
            orient="vertical",
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.task_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Right-click menu
        self.create_context_menu()
        
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Complete", command=self.complete_task)
        self.context_menu.add_command(label="Edit", command=self.edit_task)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.remove_task)
        
        self.task_tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        try:
            self.task_tree.selection_set(
                self.task_tree.identify_row(event.y)
            )
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def switch_category(self, category):
        """Enhanced category switching with visual feedback"""
        self.current_category = category
        self.category_label.config(text=category)
        
        # Update button styles
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.state(['pressed'])  # Highlight selected category
            else:
                btn.state(['!pressed'])  # Remove highlight from others
        
        # Filter and display tasks for the selected category
        self.refresh_task_list()
        
        # Update header with category-specific information
        self.update_category_header(category)
        
    def update_category_header(self, category):
        """Update header based on selected category"""
        category_info = {
            "My Day": {
                "icon": "☀️",
                "description": "Tasks for today",
                "color": "#2196F3"
            },
            "Important": {
                "icon": "⭐",
                "description": "Priority tasks",
                "color": "#F44336"
            },
            "Planned": {
                "icon": "📅",
                "description": "Scheduled tasks",
                "color": "#4CAF50"
            },
            "Personal": {
                "icon": "👤",
                "description": "Personal tasks",
                "color": "#9C27B0"
            },
            "Work": {
                "icon": "💼",
                "description": "Work-related tasks",
                "color": "#FF9800"
            },
            "Shopping": {
                "icon": "🛒",
                "description": "Shopping list",
                "color": "#00BCD4"
            }
        }
        
        info = category_info.get(category, {
            "icon": "📌",
            "description": "Task list",
            "color": "#757575"
        })
        
        # Update header with category information
        self.category_label.config(
            text=f"{info['icon']} {category}",
            foreground=info['color']
        )
        
        # Update description if it exists
        if hasattr(self, 'category_description'):
            self.category_description.config(
                text=info['description'],
                foreground=info['color']
            )
        
    def refresh_task_list(self):
        """Enhanced task list refresh with category filtering"""
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Filter tasks for current category
        category_tasks = [
            task for task in self.tasks 
            if task["category"] == self.current_category
        ]
        
        # Sort tasks based on category rules
        if self.current_category == "My Day":
            category_tasks.sort(key=lambda x: x["due_date"])
        elif self.current_category == "Important":
            category_tasks.sort(key=lambda x: (x["priority"] != "High", x["due_date"]))
        else:
            category_tasks.sort(key=lambda x: x["due_date"])
        
        # Insert tasks into tree
        for task in category_tasks:
            values = (
                task["task"],
                task["due_date"],
                task["priority"],
                task["category"],
                task["status"]
            )
            
            # Add visual indicators based on priority and status
            tags = ()
            if task["priority"] == "High":
                tags = ("high_priority",)
            if task["status"] == "Completed":
                tags = tags + ("completed",)
                
            self.task_tree.insert("", "end", values=values, tags=tags)
        
        # Update category counter
        self.update_category_counter(len(category_tasks))
        
    def update_category_counter(self, count):
        """Update the task counter for current category"""
        if hasattr(self, 'category_counter'):
            self.category_counter.config(
                text=f"{count} {'task' if count == 1 else 'tasks'}"
            )
        
    def add_task(self):
        """Enhanced add task with category assignment"""
        task = self.task_var.get().strip()
        if task:
            due_date = self.due_date.get_date().strftime("%Y-%m-%d")
            priority = self.priority_var.get()
            
            new_task = {
                "task": task,
                "due_date": due_date,
                "priority": priority,
                "category": self.current_category,
                "status": "Pending",
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # Add to Important if marked as high priority
            if priority == "High" and self.current_category != "Important":
                messagebox.showinfo(
                    "High Priority Task",
                    "This task will also appear in Important category."
                )
            
            self.tasks.append(new_task)
            self.save_tasks()
            self.refresh_task_list()
            self.task_var.set("")
            
            # Show confirmation
            messagebox.showinfo(
                "Task Added",
                f"Task added to {self.current_category}"
            )
        else:
            messagebox.showwarning(
                "Invalid Input",
                "Please enter a task!"
            )
        
    def complete_task(self):
        selected = self.task_tree.selection()
        if selected:
            item = selected[0]
            task_idx = self.task_tree.index(item)
            self.tasks[task_idx]["status"] = "Completed"
            self.save_tasks()
            self.refresh_task_list()
            
    def edit_task(self):
        selected = self.task_tree.selection()
        if selected:
            item = selected[0]
            task_idx = self.task_tree.index(item)
            task = self.tasks[task_idx]
            
            # Create edit dialog
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")
            
            ttk.Label(edit_window, text="Task:").pack(pady=5)
            task_entry = ttk.Entry(edit_window, width=40)
            task_entry.insert(0, task["task"])
            task_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="Due Date:").pack(pady=5)
            due_date = DateEntry(edit_window)
            due_date.set_date(task["due_date"])
            due_date.pack(pady=5)
            
            def save_changes():
                task["task"] = task_entry.get()
                task["due_date"] = due_date.get_date().strftime("%Y-%m-%d")
                self.save_tasks()
                self.refresh_task_list()
                edit_window.destroy()
                
            ttk.Button(
                edit_window,
                text="Save Changes",
                command=save_changes
            ).pack(pady=20)
            
    def remove_task(self):
        selected = self.task_tree.selection()
        if selected:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
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
            json.dump(self.tasks, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernToDoList(root)
    root.mainloop() 