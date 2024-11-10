import tkinter as tk
from tkinter import messagebox

class ModernToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x700")
        self.root.config(bg="black")
        
        # Initialize tasks list
        self.tasks = []
        
        # Create main layout
        self.create_main_layout()
        
    def create_main_layout(self):
        # Main frame
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(pady=30)
        
        # Task entry
        self.task_entry = tk.Entry(
            self.frame,
            font=("Helvetica", 16),
            width=35,
            bg="grey",
            fg="black",
            insertbackground="yellow"
        )
        self.task_entry.pack(pady=15)
        
        # Task list
        self.task_list = tk.Listbox(
            self.frame,
            font=("Helvetica", 16),
            width=35,
            height=15,
            bg="grey",
            fg="black",
            selectbackground="yellow",
            selectforeground="black"
        )
        self.task_list.pack(pady=15)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=30)
        
        # Buttons
        add_button = tk.Button(
            button_frame,
            text="Add Task",
            command=self.add_task,
            font=("Helvetica", 14),
            bg="yellow",
            fg="black",
            width=12
        )
        add_button.grid(row=0, column=0, padx=10, pady=5)
        
        remove_button = tk.Button(
            button_frame,
            text="Remove Task", 
            command=self.remove_task,
            font=("Helvetica", 14),
            bg="yellow",
            fg="black",
            width=12
        )
        remove_button.grid(row=0, column=1, padx=10, pady=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_tasks,
            font=("Helvetica", 14),
            bg="yellow",
            fg="black",
            width=12
        )
        clear_button.grid(row=0, column=2, padx=10, pady=5)
        
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")
            
    def remove_task(self):
        try:
            selected_index = self.task_list.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")
            
    def clear_tasks(self):
        self.tasks.clear()
        self.update_task_list()
        
    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            self.task_list.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernToDoList(root)
    root.mainloop()