import tkinter as tk
import os
from tkinter import ttk, messagebox, font, simpledialog

TASKS_FILE = "tasks.txt"

def load_tasks():
    try:
        os.system("attrib -h tasks.txt")
        with open(TASKS_FILE, "r") as file:
            return [line.strip().split("|") for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        os.system("attrib -h tasks.txt")
        file.write("\n".join(["|".join(task) for task in tasks]))

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append([task, "0"])  # ["Task Name", "0" (incomplete)]
        save_tasks()
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    task_name = remove_entry.get().strip()
    for task in tasks:
        if task[0] == task_name:
            tasks.remove(task)
            save_tasks()
            update_task_list()
            remove_entry.delete(0, tk.END)
            return
    messagebox.showwarning("Warning", "Task not found!")

def toggle_task_completion(index):
    tasks[index][1] = "1" if tasks[index][1] == "0" else "0"  # Toggle completion status
    save_tasks()
    update_task_list()

def edit_task(index):
    current_task = tasks[index][0]
    new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task)
    if new_task and new_task.strip():
        tasks[index][0] = new_task.strip()
        save_tasks()
        update_task_list()

def update_task_list():
    # Clear the task list
    for widget in task_list_frame.winfo_children():
        widget.destroy()

    # Add tasks to the list
    for i, task in enumerate(tasks):
        task_text = task[0]
        task_status = task[1]

        # Create a frame for each task
        task_frame = tk.Frame(task_list_frame, bg="#2c3e50")
        task_frame.pack(fill=tk.X, pady=5, padx=10)

        # Add a checkbox (using a Label)
        checkbox = tk.Label(task_frame, text="☑" if task_status == "1" else "☐", 
                            fg="#2ecc71" if task_status == "1" else "#e74c3c", 
                            bg="#2c3e50", font=("Arial", 20))  # Bigger checkbox
        checkbox.pack(side=tk.LEFT, padx=10)
        checkbox.bind("<Button-1>", lambda e, idx=i: toggle_task_completion(idx))

        # Add the task text (with strikethrough if completed)
        task_label = tk.Label(task_frame, text=task_text, 
                              fg="#7f8c8d" if task_status == "1" else "#ecf0f1", 
                              bg="#2c3e50", font=("Arial", 16))  # Bigger task text
        if task_status == "1":
            task_label.config(font=("Arial", 16, "overstrike"))
        task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        task_label.bind("<Double-Button-1>", lambda e, idx=i: edit_task(idx))

def clear_tasks():
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
        tasks.clear()
        save_tasks()
        update_task_list()

tasks = load_tasks()

root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.configure(bg="#1e272e")
custom_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

entry_frame = tk.Frame(root, bg="#1e272e")
entry_frame.pack(pady=10, fill=tk.X)

task_entry = ttk.Entry(entry_frame, width=30, font=custom_font)
task_entry.grid(row=0, column=0, padx=10, pady=5, ipady=5)

add_button = tk.Button(entry_frame, text="➕ Add Task", command=add_task, bg="#3498db", fg="white", 
                       font=button_font, bd=0, padx=10, pady=5, relief=tk.FLAT)
add_button.grid(row=0, column=1, padx=10)
add_button.bind("<Enter>", lambda e: add_button.config(bg="#2980b9"))
add_button.bind("<Leave>", lambda e: add_button.config(bg="#3498db"))

list_frame = tk.Frame(root, bg="#1e272e")
list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Use a Canvas and Frame for scrollable task list
canvas = tk.Canvas(list_frame, bg="#2c3e50", highlightthickness=0)
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
task_list_frame = tk.Frame(canvas, bg="#2c3e50")

task_list_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=task_list_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

remove_entry = ttk.Entry(entry_frame, width=30, font=custom_font)
remove_entry.grid(row=1, column=0, padx=10, pady=5, ipady=5)

remove_button = tk.Button(entry_frame, text="➖ Remove Task", command=remove_task, 
                          bg="#e74c3c", fg="white", font=button_font, bd=0, padx=10, pady=5, relief=tk.FLAT)
remove_button.grid(row=1, column=1, padx=10)
remove_button.bind("<Enter>", lambda e: remove_button.config(bg="#c0392b"))
remove_button.bind("<Leave>", lambda e: remove_button.config(bg="#e74c3c"))

# Add a label under the remove button
note_label = tk.Label(root, text="Note: You can double click to edit tasks", 
                      bg="#1e272e", fg="#7f8c8d", font=("Helvetica", 10))
note_label.pack(pady=5)

clear_button = tk.Button(root, text="🧹 Clear All", command=clear_tasks, 
                         bg="#95a5a6", fg="white", font=button_font, bd=0, padx=10, pady=5, relief=tk.FLAT)
clear_button.pack(pady=10)
clear_button.bind("<Enter>", lambda e: clear_button.config(bg="#7f8c8d"))
clear_button.bind("<Leave>", lambda e: clear_button.config(bg="#95a5a6"))

update_task_list()

root.mainloop()
