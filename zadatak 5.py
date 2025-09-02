## Zadatak 5. Kalkulator
# Razvijte jednostavnu aplikaciju kalkulatora s Tkinterom. Aplikacija treba imati gumbe za brojeve (0–9) i osnovne operacije (+, −, *, /). Korisnik treba moći unijeti izraz i vidjeti rezultat proračuna.

# **Smjernice**
# - Koristite se widgetom `Entry` za unos i prikaz rezultata.
# - Implementirajte osnovne matematičke operacije.

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Zadatak 5")
root.geometry("400x400")


def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        print(e)



number_buttons = []
for i in range(10):
    button = ttk.Button(root, text=str(i), command=lambda i=i: entry.insert(tk.END, str(i)))
    number_buttons.append(button)

for i, button in enumerate(number_buttons):
    button.grid(row=1, column=i, sticky="nsew")

    

operation_buttons = []
for op in ["+", "-", "*", "/", ".", "C"]:
    button = ttk.Button(root, text=op, command=lambda op=op: entry.insert(tk.END, op))
    operation_buttons.append(button)

entry = ttk.Entry(root)
entry.pack(pady=10)




root.grid_columnconfigure(0, weight=1)
root.mainloop()