## Zadatak 3. Čitač tekstualnih datoteka
# Kreirajte aplikaciju Tkinter koja ima polje za unos putanje do datoteke i gumb „Učitaj datoteku”. 
# Nakon klika na gumb, sadržaj tekstualne datoteke trebao bi se prikazati u `Text` widgetu unutar aplikacije.

# **Smjernice**
# - Upotrijebite `Entry` za unos putanje do datoteke.
# - Upotrijebite widget `Text` za prikaz sadržaja datoteke.
# - Implementirajte funkciju koja čita sadržaj datoteke i prikazuje ga widgetu u `Text`.

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Zadatak tri")
root.geometry("400x300")

def load_file():
    file_path = entry.get()
    file_path = file_path.strip().replace('"', '')
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
    except Exception as e:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Greška pri otvaranju datoteke:\n{e}")


entry = ttk.Entry(root, width=50)
entry.pack(pady=20)

load_button = ttk.Button(root, text="Učitaj datoteku", command=load_file)
load_button.pack()

text_widget = tk.Text(root)
text_widget.pack()


root.mainloop()
