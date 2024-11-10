import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CategoryPage(ttk.Frame):
    def __init__(self, parent, category_name, main_app):
        super().__init__(parent)
        self.category_name = category_name
        self.main_app = main_app
        
        # Configure modern theme colors
        self.configure(style='Modern.TFrame')
        style = ttk.Style()
        style.configure('Modern.TFrame', background='#F0F2F5')  # Light gray background
        style.configure('Modern.TLabel', background='#F0F2F5', foreground='#1A1A1A')  # Dark gray text
        style.configure('Modern.TButton', background='#0078D4', foreground='white')  # Microsoft blue
        style.configure('Task.TEntry', fieldbackground='white', foreground='#1A1A1A')
        style.configure('Modern.Treeview', 
                       background='white',
                       fieldbackground='white', 
                       foreground='#1A1A1A')
        style.configure('Modern.Treeview.Heading',
                       background='#E6E6E6',  # Light gray headers
                       foreground='#1A1A1A')
        
        self.create_page()
        
    def create_page(self):
        # Header with subtle gradient effect
        header_frame = ttk.Frame(self, style='Modern.TFrame')
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Category title with icon and modern font
        icon_map = {
            "My Day": "☀️",
            "Important": "⭐",
            "Planned": "📅", 
            "Personal": "👤",
            "Work": "💼",
            "Shopping": "🛒"
        }
        
        title = ttk.Label(
            header_frame,
            text=f"{icon_map.get(self.category_name, '📌')} {self.category_name}",
            font=("Segoe UI", 28, "bold"),
            style='Modern.TLabel'
        )
        title.pack(side="left", padx=20)
        
        # Add task section with modern styling
        self.create_task_input()
        
        # Tasks list with custom styling
        self.create_tasks_list()

        # Add completed tasks section if My Day category
        if self.category_name == "My Day":
            self.create_completed_tasks_list()
        
    def create_task_input(self):
        input_frame = ttk.Frame(self, style='Modern.TFrame')
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Modern task entry
        self.task_var = tk.StringVar()
        task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=("Segoe UI", 12),
            width=40,
            style='Task.TEntry'
        )
        task_entry.pack(side="left", padx=(0, 10))
        
        # Styled date picker
        self.due_date = DateEntry(
            input_frame,
            width=12,
            background='white',
            foreground='#1A1A1A',
            borderwidth=1,
            selectbackground='#0078D4'
        )
        self.due_date.pack(side="left", padx=5)
        
        # Modern priority selector
        self.priority_var = tk.StringVar(value="Normal")
        priorities = ["Low", "Normal", "High"]
        priority_menu = ttk.OptionMenu(
            input_frame,
            self.priority_var,
            "Normal",
            *priorities,
            style='Modern.TButton'
        )
        priority_menu.pack(side="left", padx=5)
        
        # Stylish add button
        add_btn = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_task,
            style='Modern.TButton'
        )
        add_btn.pack(side="left", padx=5)
        
    def create_tasks_list(self):
        # Tasks container with modern theme
        list_frame = ttk.Frame(self, style='Modern.TFrame')
        list_frame.pack(fill="both", expand=True, padx=20)

        # Modern label for active tasks
        if self.category_name == "My Day":
            ttk.Label(list_frame, 
                     text="Active Tasks", 
                     font=("Segoe UI", 14, "bold"),
                     style='Modern.TLabel').pack(anchor="w", pady=(0,10))
        
        # Styled Treeview
        columns = ("Complete", "Task", "Due Date", "Priority", "Status")
        self.task_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style='Modern.Treeview'
        )
        
        # Configure modern columns
        self.task_tree.heading("Complete", text="")
        self.task_tree.column("Complete", width=30)
        for col in columns[1:]:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=150)
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.task_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind checkbox click
        self.task_tree.bind('<Button-1>', self.on_checkbox_click)
        
        # Context menu
        self.create_context_menu()

    def on_checkbox_click(self, event):
        region = self.task_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.task_tree.identify_column(event.x)
            if column == '#1':  # Complete column
                item = self.task_tree.identify_row(event.y)
                if item:
                    self.complete_task(item)

    def create_completed_tasks_list(self):
        # Completed tasks container with modern theme
        completed_frame = ttk.Frame(self, style='Modern.TFrame')
        completed_frame.pack(fill="both", expand=True, padx=20, pady=(20,0))

        # Modern label for completed tasks
        ttk.Label(completed_frame, 
                 text="Completed Tasks", 
                 font=("Segoe UI", 14, "bold"),
                 style='Modern.TLabel').pack(anchor="w", pady=(0,10))

        # Styled Treeview for completed tasks
        columns = ("Complete", "Task", "Due Date", "Priority", "Status")
        self.completed_tree = ttk.Treeview(
            completed_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            style='Modern.Treeview'
        )
        
        # Configure modern columns
        self.completed_tree.heading("Complete", text="")
        self.completed_tree.column("Complete", width=30)
        for col in columns[1:]:
            self.completed_tree.heading(col, text=col)
            self.completed_tree.column(col, width=150)
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(
            completed_frame,
            orient="vertical",
            command=self.completed_tree.yview
        )
        self.completed_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.completed_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0, bg='white', fg='#1A1A1A')
        if self.category_name == "My Day":
            self.context_menu.add_command(label="✓ Mark Complete", command=lambda: self.complete_task(self.task_tree.selection()[0]))
        else:
            self.context_menu.add_command(label="Complete", command=lambda: self.complete_task(self.task_tree.selection()[0]))
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
            
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            try:
                # Create new task with all required fields
                new_task = {
                    "task": task,
                    "due_date": self.due_date.get_date().strftime("%Y-%m-%d"),
                    "priority": self.priority_var.get(),
                    "category": self.category_name,
                    "status": "Pending",
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                self.main_app.tasks.append(new_task)
                self.main_app.save_tasks()
                self.refresh_tasks()
                self.task_var.set("")
                messagebox.showinfo("Success", "Task added successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error adding task: {str(e)}")
        else:
            messagebox.showwarning("Invalid Input", "Please enter a task!")
            
    def complete_task(self, item):
        values = self.task_tree.item(item)['values']
        task_name = values[1]  # Task is now in second column
        
        for task in self.main_app.tasks:
            if (task["category"] == self.category_name and 
                task["task"] == task_name and
                task["status"] != "Completed"):
                task["status"] = "Completed"
                self.main_app.save_tasks()
                self.refresh_tasks()
                break
            
    def edit_task(self):
        selected = self.task_tree.selection()
        if selected:
            item = selected[0]
            values = self.task_tree.item(item)['values']
            
            # Create modern edit dialog
            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")
            edit_window.configure(bg='#F0F2F5')
            
            ttk.Label(edit_window, text="Task:", style='Modern.TLabel').pack(pady=5)
            task_entry = ttk.Entry(edit_window, width=40, style='Task.TEntry')
            task_entry.insert(0, values[1])
            task_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="Due Date:", style='Modern.TLabel').pack(pady=5)
            due_date = DateEntry(edit_window, 
                               background='white',
                               foreground='#1A1A1A',
                               borderwidth=1)
            due_date.set_date(values[2])
            due_date.pack(pady=5)
            
            def save_changes():
                for task in self.main_app.tasks:
                    if (task["category"] == self.category_name and 
                        task["task"] == values[1]):
                        task["task"] = task_entry.get()
                        task["due_date"] = due_date.get_date().strftime("%Y-%m-%d")
                        break
                self.main_app.save_tasks()
                self.refresh_tasks()
                edit_window.destroy()
                
            ttk.Button(
                edit_window,
                text="Save Changes",
                command=save_changes,
                style='Modern.TButton'
            ).pack(pady=20)
            
    def remove_task(self):
        selected = self.task_tree.selection()
        if selected:
            if messagebox.askyesno("Confirm Delete", "Delete this task?"):
                item = selected[0]
                values = self.task_tree.item(item)['values']
                self.main_app.tasks = [
                    task for task in self.main_app.tasks 
                    if not (task["category"] == self.category_name and 
                           task["task"] == values[1])
                ]
                self.main_app.save_tasks()
                self.refresh_tasks()
                
    def refresh_tasks(self):
        # Clear existing tasks
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        if hasattr(self, 'completed_tree'):
            for item in self.completed_tree.get_children():
                self.completed_tree.delete(item)
        
        try:
            # Filter tasks for current category
            category_tasks = [
                task for task in self.main_app.tasks 
                if task.get("category", "") == self.category_name
            ]
            
            # Split into active and completed tasks
            active_tasks = [task for task in category_tasks if task.get("status") != "Completed"]
            completed_tasks = [task for task in category_tasks if task.get("status") == "Completed"]
            
            # Add active tasks to main tree
            for task in active_tasks:
                values = (
                    "☐",
                    task.get("task", ""),
                    task.get("due_date", ""),
                    task.get("priority", "Normal"),
                    task.get("status", "Pending")
                )
                self.task_tree.insert("", "end", values=values)

            # Add completed tasks to completed tree if in My Day category
            if hasattr(self, 'completed_tree'):
                for task in completed_tasks:
                    values = (
                        "✓",
                        task.get("task", ""),
                        task.get("due_date", ""),
                        task.get("priority", "Normal"),
                        task.get("status", "Completed")
                    )
                    self.completed_tree.insert("", "end", values=values)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tasks: {str(e)}")

class DashboardPage(ttk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        
        # Configure modern theme
        style = ttk.Style()
        style.configure('Modern.TFrame', background='#F0F2F5')
        style.configure('Modern.TLabel', background='#F0F2F5', foreground='#1A1A1A')
        
        self.create_dashboard()
        
    def create_dashboard(self):
        # Title with modern styling
        title = ttk.Label(
            self,
            text="Task Analytics Dashboard",
            font=("Segoe UI", 28, "bold"),
            style='Modern.TLabel'
        )
        title.pack(pady=20)
        
        # Create graphs container
        graphs_frame = ttk.Frame(self, style='Modern.TFrame')
        graphs_frame.pack(fill="both", expand=True, padx=20)
        
        # Create left and right frames for graphs
        left_frame = ttk.Frame(graphs_frame, style='Modern.TFrame')
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = ttk.Frame(graphs_frame, style='Modern.TFrame')
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Create modern graphs
        self.create_completion_pie_chart(left_frame)
        self.create_category_bar_graph(right_frame)
        
        # Create summary section
        self.create_summary_section()
        
    def create_completion_pie_chart(self, parent):
        # Create figure with a modern style
        plt.style.use('default')  # Using default style instead of seaborn
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#F5F5F5')
        
        # Calculate completion stats
        completed = sum(1 for task in self.main_app.tasks 
                       if task.get("status") == "Completed")
        pending = len(self.main_app.tasks) - completed
        
        # Create pie chart with modern colors
        sizes = [completed, pending]
        labels = ['Completed', 'Pending']
        colors = ['#2ECC71', '#E74C3C']  # Modern green and red
        
        # Add shadow and explosion effects
        explode = (0.05, 0)  # Slightly explode the first slice
        
        wedges, texts, autotexts = ax.pie(sizes, 
                                         explode=explode,
                                         labels=labels, 
                                         colors=colors,
                                         autopct='%1.1f%%',
                                         shadow=True,
                                         startangle=90)
        
        # Enhance text properties
        plt.setp(autotexts, size=9, weight="bold")
        plt.setp(texts, size=10)
        
        # Add title with custom styling
        ax.set_title("Task Completion Status", 
                    pad=20, 
                    fontsize=12, 
                    fontweight='bold')
        
        # Equal aspect ratio ensures circular plot
        ax.axis('equal')
        
        # Create canvas with tight layout
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
    def create_category_bar_graph(self, parent):
        # Use default style
        plt.style.use('default')
        
        # Create figure
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#F5F5F5')
        
        # Calculate category stats
        categories = ["My Day", "Important", "Planned", "Personal", "Work", "Shopping"]
        completed_counts = []
        pending_counts = []
        
        for category in categories:
            category_tasks = [task for task in self.main_app.tasks 
                            if task.get("category") == category]
            completed = sum(1 for task in category_tasks 
                          if task.get("status") == "Completed")
            pending = len(category_tasks) - completed
            completed_counts.append(completed)
            pending_counts.append(pending)
        
        # Create bar chart with modern styling
        x = range(len(categories))
        width = 0.35
        
        # Add bars with enhanced styling
        completed_bars = ax.bar([i - width/2 for i in x], 
                                completed_counts, 
                                width,
                                label='Completed',
                                color='#2ECC71',
                                alpha=0.8)
        
        pending_bars = ax.bar([i + width/2 for i in x], 
                            pending_counts, 
                            width,
                            label='Pending',
                            color='#E74C3C',
                            alpha=0.8)
        
        # Customize chart appearance
        ax.set_ylabel('Number of Tasks', fontsize=10)
        ax.set_title('Tasks by Category', fontsize=12, pad=20, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        
        # Add value labels on top of bars
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{int(height)}',
                           xy=(rect.get_x() + rect.get_width() / 2, height),
                           xytext=(0, 3),  # 3 points vertical offset
                           textcoords="offset points",
                           ha='center',
                           va='bottom',
                           fontsize=8)
        
        autolabel(completed_bars)
        autolabel(pending_bars)
        
        # Enhance legend
        ax.legend(loc='upper right', frameon=True)
        
        # Add grid for better readability
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        
        # Adjust layout
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
    def create_summary_section(self):
        summary_frame = ttk.Frame(self, style='Modern.TFrame')
        summary_frame.pack(fill="x", padx=20, pady=20)
        
        # Calculate statistics
        total_tasks = len(self.main_app.tasks)
        completed_tasks = sum(1 for task in self.main_app.tasks 
                            if task.get("status") == "Completed")
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Today's tasks
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = sum(1 for task in self.main_app.tasks 
                         if task.get("due_date") == today)
        
        # Create modern summary labels
        summaries = [
            f"Total Tasks: {total_tasks}",
            f"Completed Tasks: {completed_tasks}",
            f"Completion Rate: {completion_rate:.1f}%",
            f"Tasks Due Today: {today_tasks}"
        ]
        
        # Create and style modern labels
        for summary in summaries:
            label = ttk.Label(
                summary_frame,
                text=summary,
                font=("Segoe UI", 12),
                style='Modern.TLabel'
            )
            label.pack(side="left", padx=20)
            
    def refresh_dashboard(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Recreate dashboard
        self.create_dashboard()

class ModernToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Task Manager")
        self.root.geometry("1200x800")
        
        # Initialize tasks list
        self.tasks = self.load_tasks()
        self.current_category = "My Day"
        
        # Apply modern styles
        self.apply_modern_styles()
        
        # Create UI components
        self.create_modern_sidebar()
        self.create_modern_content()
        
    def add_task(self):
        """Add a new task to the list"""
        task = self.task_var.get().strip()
        if task:
            try:
                # Create new task with all required fields
                new_task = {
                    "task": task,
                    "due_date": datetime.now().strftime("%Y-%m-%d"),
                    "priority": "Normal",
                    "category": self.current_category,
                    "status": "Pending",
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                self.tasks.append(new_task)
                self.save_tasks()
                self.refresh_task_list()
                self.task_var.set("")  # Clear input
                
                messagebox.showinfo(
                    "Success",
                    f"Task added to {self.current_category}"
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Error adding task: {str(e)}"
                )
        else:
            messagebox.showwarning(
                "Invalid Input",
                "Please enter a task!"
            )
    
    def remove_task(self):
        """Remove selected task"""
        selected = self.task_tree.selection()
        if selected:
            if messagebox.askyesno("Confirm Delete", "Delete this task?"):
                item = selected[0]
                values = self.task_tree.item(item)['values']
                self.tasks = [
                    task for task in self.tasks 
                    if not (task["task"] == values[0] and 
                           task["category"] == self.current_category)
                ]
                self.save_tasks()
                self.refresh_task_list()
    
    def complete_task(self):
        """Mark selected task as completed"""
        selected = self.task_tree.selection()
        if selected:
            item = selected[0]
            values = self.task_tree.item(item)['values']
            for task in self.tasks:
                if (task["task"] == values[0] and 
                    task["category"] == self.current_category):
                    task["status"] = "Completed"
                    break
            self.save_tasks()
            self.refresh_task_list()
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        category_tasks = [
            task for task in self.tasks 
            if task.get("category") == self.current_category
        ]
        
        for task in category_tasks:
            values = (
                task.get("task", ""),
                task.get("due_date", ""),
                task.get("priority", "Normal"),
                task.get("status", "Pending")
            )
            
            # Add tags for styling
            tags = ()
            if task.get("status") == "Completed":
                tags = ("completed",)
            elif task.get("priority") == "High":
                tags = ("high_priority",)
                
            self.task_tree.insert("", "end", values=values, tags=tags)
    
    def load_tasks(self):
        """Load tasks from file"""
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
            return []
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error loading tasks: {str(e)}"
            )
            return []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open("tasks.json", "w") as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error saving tasks: {str(e)}"
            )
    
    def show_page(self, category):
        """Switch to selected category page"""
        self.current_category = category
        self.refresh_task_list()
        
        # Update UI to show selected category
        if hasattr(self, 'category_label'):
            self.category_label.config(text=category)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernToDoList(root)
    root.mainloop()