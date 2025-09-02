
# Zadatak 2. Brojač 
# Razvijte aplikaciju Tkinter koja prikazuje broj u labelu i ima dva gumba označena s „Povećaj” i „Smanji”. 
# Svaki put kada se klikne na gumb, broj prikazan u labelu treba se povećati ili smanjiti za 1. 

# Smjernice:  
# • Upotrijebite „IntVar” za pohranu i praćenje promjena broja. 
# • Ažurirajte vrijednost prikazanu u labelu nakon svakog klika na gumb. 


import tkinter as tk
from tkinter import ttk
 
def povecaj():
    return broj.set(broj.get() + 1) 
 
 
def smanji():
    return broj.set(broj.get() - 1) 
 
 
root = tk.Tk()
root.geometry("250x150")
root.title("Zadatak dva")
 
broj = tk.IntVar(value=200)
 
label = tk.Label(root, textvariable=broj)
label.pack()
 
button = tk.Button(root, text="Povećaj!", command=povecaj)
button.pack(side='right')
 
button = tk.Button(root, text="Smanji!", command=smanji)
button.pack(side='left')
 
root.mainloop()