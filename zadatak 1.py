# Zadatak 1. Jednostavna aplikacija „Pozdrav svijetu”
# Zadatak
# Kreirajte osnovnu aplikaciju Tkinter s jednim gumbom. Kada korisnik klikne na gumb, aplikacija bi trebala
# prikazati tekst „Pozdrav, svijete!” u labelu ispod gumba.
# Smjernice:
# • Upotrijebite „Label” za prikazivanje teksta.
# • Upotrijebite „Button” za interakciju s korisnikom.
# • Implementirajte funkciju koja mijenja tekst u oznaci (labelu) nakon klika na gumb.


import tkinter as tk
from tkinter import ttk
 
 
def show_data():
     label.config(text="Pozdrav svijete!")
 
 
root = tk.Tk()
root.title("Prvi zadatak")
 
button = ttk.Button(root, text="Pritisni", command=show_data)
button.grid(row=2, column=1, columnspan=3, pady=20)
label = tk.Label(root, text="")
label.grid(row=0, column=2, rowspan=2, padx=10, pady=5)
 
root.mainloop()