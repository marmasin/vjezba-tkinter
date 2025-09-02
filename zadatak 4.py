## Zadatak 4. To-Do lista
# Izradite aplikaciju za upravljanje to-do listom u kojoj korisnici mogu dodavati zadatke, označavati ih kao dovršene i brisati ih. 
# Zadaci trebaju biti pohranjeni u tekstualnoj datoteci, a aplikacija treba učitavati postojeće zadatke pri pokretanju.

# **Smjernice**
# - Upotrijebite `Listbox` za prikaz zadataka.
# - Implementirajte funkcije za dodavanje, brisanje i spremanje zadataka.
# - Koristite se tekstualnom datotekom za pohranu zadataka.


import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("zadatak 4")
root.geometry("400x400")


def load_tasks():
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            tasks = file.readlines()
            for task in tasks:
                listbox.insert(tk.END, task.strip())
    except FileNotFoundError:
        pass

def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        tasks = listbox.get(0, tk.END)
        for task in tasks:
            file.write(task + "\n")

def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()

def delete_task():
    selected_tasks = listbox.curselection()
    for index in reversed(selected_tasks):
        listbox.delete(index)
    save_tasks()

listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack(pady=10)

delete_button = ttk.Button(root, text="Obriši zadatak", command=delete_task)
delete_button.pack(pady=5)

add_button = ttk.Button(root, text="Dodaj zadatak", command=add_task)
add_button.pack(pady=5)

entry = ttk.Entry(root)
entry.pack(pady=5)

load_tasks()

root.mainloop()
