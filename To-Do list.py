import tkinter as tk
from tkinter import ttk, messagebox, font

TASKS_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_tasks():
    with open(TASKS_FILE, "w") as file:
        file.write("\n".join(tasks))

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append(task)
        save_tasks()
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    task_name = remove_entry.get().strip()
    if task_name in tasks:
        tasks.remove(task_name)
        save_tasks()
        update_task_list()
        remove_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task not found!")

def update_task_list():
    task_list.delete(0, tk.END)
    for i, task in enumerate(tasks, 1):
        task_list.insert(tk.END, f"{i}. {task}")
        if i % 2 == 0:
            task_list.itemconfig(tk.END, bg="#34495e", fg="#ecf0f1")
        else:
            task_list.itemconfig(tk.END, bg="#2c3e50", fg="#ecf0f1")

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

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=custom_font, 
                       bg="#2c3e50", fg="#ecf0f1", selectbackground="#3498db", 
                       selectforeground="white", bd=0, highlightthickness=0)
task_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=task_list.yview)

remove_entry = ttk.Entry(entry_frame, width=30, font=custom_font)
remove_entry.grid(row=1, column=0, padx=10, pady=5, ipady=5)

remove_button = tk.Button(entry_frame, text="➖ Remove Task", command=remove_task, 
                          bg="#e74c3c", fg="white", font=button_font, bd=0, padx=10, pady=5, relief=tk.FLAT)
remove_button.grid(row=1, column=1, padx=10)
remove_button.bind("<Enter>", lambda e: remove_button.config(bg="#c0392b"))
remove_button.bind("<Leave>", lambda e: remove_button.config(bg="#e74c3c"))

clear_button = tk.Button(root, text="🧹 Clear All", command=clear_tasks, 
                         bg="#95a5a6", fg="white", font=button_font, bd=0, padx=10, pady=5, relief=tk.FLAT)
clear_button.pack(pady=10)
clear_button.bind("<Enter>", lambda e: clear_button.config(bg="#7f8c8d"))
clear_button.bind("<Leave>", lambda e: clear_button.config(bg="#95a5a6"))

update_task_list()

root.mainloop()