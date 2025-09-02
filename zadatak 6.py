## Zadatak 6. Upravljanje kontaktima s SQLite bazom
# Razvijte aplikaciju za upravljanje kontaktima. 
# Korisnici mogu dodavati, uređivati, brisati i pretraživati kontakte. Podatci o kontaktima (ime, prezime, broj telefona, e-pošta) trebaju biti pohranjeni u SQLite bazi podataka.

# **Smjernice**
# - Koristite se SQLite bazom za pohranu podataka.
# - Kreirajte sučelje za prikazivanje, dodavanje i uređivanje kontakata.
# - Implementirajte funkcionalnost za pretraživanje i filtriranje kontakata.
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Provjera postojanja baze podataka i kreiranje ako ne postoji
def kreiraj_bazu():
    """
    Kreira 'kontakti.db' datoteku baze podataka i 'kontakti' tablicu ako ne postoje.
    """
    conn = sqlite3.connect('kontakti.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kontakti (
            id INTEGER PRIMARY KEY,
            ime TEXT NOT NULL,
            prezime TEXT NOT NULL,
            broj_telefona TEXT,
            e_posta TEXT
        )
    ''')
    conn.commit()
    conn.close()

class AplikacijaKontakti(tk.Tk):
    """
    Glavna klasa aplikacije koja stvara GUI i upravlja interakcijom
    s bazom podataka.
    """
    def __init__(self):
        super().__init__()
        self.title("Upravljanje kontaktima")
        self.geometry("850x600")

        # Povezivanje s bazom podataka
        self.db_conn = sqlite3.connect('kontakti.db')
        self.cursor = self.db_conn.cursor()
        
        # Inicijalizacija sučelja
        self.kreiraj_sučelje()
        self.prikazi_sve_kontakte()

    def kreiraj_sučelje(self):
        """
        Stvara sve GUI elemente: polja za unos, gumbe, tablicu.
        """
        # Okvir za unos podataka
        unos_okvir = ttk.LabelFrame(self, text="Podaci o kontaktu")
        unos_okvir.pack(padx=10, pady=10, fill="x")

        # Labele i polja za unos
        tk.Label(unos_okvir, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.ime_unos = tk.Entry(unos_okvir)
        self.ime_unos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(unos_okvir, text="Prezime:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.prezime_unos = tk.Entry(unos_okvir)
        self.prezime_unos.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        tk.Label(unos_okvir, text="Broj_telefona:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.broj_telefona_unos = tk.Entry(unos_okvir)
        self.broj_telefona_unos.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(unos_okvir, text="E-pošta:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.eposta_unos = tk.Entry(unos_okvir)
        self.eposta_unos.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        # Povezivanje okvira s grid-om
        unos_okvir.grid_columnconfigure(1, weight=1)
        unos_okvir.grid_columnconfigure(3, weight=1)

        # Okvir za gumbe
        gumbi_okvir = ttk.Frame(self)
        gumbi_okvir.pack(pady=5)
        
        # Gumbi za akcije
        ttk.Button(gumbi_okvir, text="Dodaj", command=self.dodaj_kontakt).pack(side=tk.LEFT, padx=5)
        ttk.Button(gumbi_okvir, text="Ažuriraj", command=self.azuriraj_kontakt).pack(side=tk.LEFT, padx=5)
        ttk.Button(gumbi_okvir, text="Obriši", command=self.obrisi_kontakt).pack(side=tk.LEFT, padx=5)
        ttk.Button(gumbi_okvir, text="Očisti polja", command=self.ocisti_polja).pack(side=tk.LEFT, padx=5)
        
        # Okvir za pretragu
        pretraga_okvir = ttk.Frame(self)
        pretraga_okvir.pack(pady=5, fill="x", padx=10)
        
        ttk.Label(pretraga_okvir, text="Pretraga po imenu/prezimenu:").pack(side=tk.LEFT, padx=(0, 5))
        self.pretraga_unos = tk.Entry(pretraga_okvir)
        self.pretraga_unos.pack(side=tk.LEFT, fill="x", expand=True)
        self.pretraga_unos.bind("<KeyRelease>", self.pretrazi) # Filtriranje u realnom vremenu

        # Tablica za prikaz kontakata
        stupci = ("ID", "Ime", "Prezime", "broj_telefona", "E-pošta")
        self.tree = ttk.Treeview(self, columns=stupci, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for stupac in stupci:
            self.tree.heading(stupac, text=stupac, anchor="w")
            self.tree.column(stupac, width=150, minwidth=100)
        
        # Postavljanje kolone ID-a da bude uža
        self.tree.column("ID", width=50, minwidth=40, stretch=tk.NO)

        # Učitavanje podataka iz odabranog retka u polja za unos
        self.tree.bind('<<TreeviewSelect>>', self.ucitaj_u_polja)

    def prikazi_sve_kontakte(self):
        """
        Dohvaća sve kontakte iz baze podataka i prikazuje ih u tablici.
        """
        # Briše sve postojeće unose u tablici
        for redak in self.tree.get_children():
            self.tree.delete(redak)
        
        self.cursor.execute('SELECT * FROM kontakti ORDER BY prezime, ime')
        kontakti = self.cursor.fetchall()
        
        for kontakt in kontakti:
            self.tree.insert("", "end", values=kontakt)

    def dodaj_kontakt(self):
        """
        Dodaje novi kontakt u bazu podataka.
        """
        ime = self.ime_unos.get().strip()
        prezime = self.prezime_unos.get().strip()
        broj_telefona = self.broj_telefona_unos.get().strip()
        eposta = self.eposta_unos.get().strip()
        
        if not ime or not prezime:
            messagebox.showerror("Greška", "Ime i prezime su obavezna polja.")
            return

        self.cursor.execute('''
            INSERT INTO kontakti (ime, prezime, broj_telefona, e_posta)
            VALUES (?, ?, ?, ?)
        ''', (ime, prezime, broj_telefona, eposta))
        self.db_conn.commit()
        messagebox.showinfo("Uspjeh", "Kontakt uspješno dodan!")
        self.ocisti_polja()
        self.prikazi_sve_kontakte()

    def azuriraj_kontakt(self):
        """
        Ažurira odabrani kontakt u bazi podataka.
        """
        odabrano = self.tree.focus()
        if not odabrano:
            messagebox.showerror("Greška", "Odaberite kontakt za ažuriranje.")
            return

        kontakt_id = int(self.tree.item(odabrano, 'values')[0])
        novo_ime = self.ime_unos.get().strip()
        novo_prezime = self.prezime_unos.get().strip()
        novi_broj_telefona = self.broj_telefona_unos.get().strip()
        nova_eposta = self.eposta_unos.get().strip()
        
        if not novo_ime or not novo_prezime:
            messagebox.showerror("Greška", "Ime i prezime su obavezna polja.")
            return

        self.cursor.execute('''
            UPDATE kontakti
            SET ime = ?, prezime = ?, broj_telefona = ?, e_posta = ?
            WHERE id = ?
        ''', (novo_ime, novo_prezime, novi_broj_telefona, nova_eposta, kontakt_id))
        self.db_conn.commit()
        messagebox.showinfo("Uspjeh", "Kontakt uspješno ažuriran!")
        self.ocisti_polja()
        self.prikazi_sve_kontakte()
    
    def obrisi_kontakt(self):
        """
        Briše odabrani kontakt iz baze podataka nakon potvrde.
        """
        odabrano = self.tree.focus()
        if not odabrano:
            messagebox.showerror("Greška", "Odaberite kontakt za brisanje.")
            return
        
        kontakt_id = int(self.tree.item(odabrano, 'values')[0])
        
        if messagebox.askyesno("Potvrda brisanja", "Jeste li sigurni da želite obrisati ovaj kontakt?"):
            self.cursor.execute('DELETE FROM kontakti WHERE id = ?', (kontakt_id,))
            self.db_conn.commit()
            messagebox.showinfo("Uspjeh", "Kontakt uspješno obrisan!")
            self.ocisti_polja()
            self.prikazi_sve_kontakte()

    def pretrazi(self, event=None):
        """
        Pretražuje kontakte u bazi podataka na temelju pojma za pretragu.
        """
        pojam = self.pretraga_unos.get().strip()
        
        # Briše postojeće unose u tablici
        for redak in self.tree.get_children():
            self.tree.delete(redak)
            
        if pojam:
            self.cursor.execute('''
                SELECT * FROM kontakti
                WHERE ime LIKE ? OR prezime LIKE ?
                ORDER BY prezime, ime
            ''', ('%' + pojam + '%', '%' + pojam + '%'))
            rezultati = self.cursor.fetchall()
            for kontakt in rezultati:
                self.tree.insert("", "end", values=kontakt)
        else:
            self.prikazi_sve_kontakte()

    def ucitaj_u_polja(self, event):
        """
        Učitava podatke odabranog kontakta u polja za unos.
        """
        odabrano = self.tree.focus()
        if odabrano:
            vrijednosti = self.tree.item(odabrano, 'values')
            self.ocisti_polja()
            self.ime_unos.insert(0, vrijednosti[1])
            self.prezime_unos.insert(0, vrijednosti[2])
            self.broj_telefona_unos.insert(0, vrijednosti[3])
            self.eposta_unos.insert(0, vrijednosti[4])

    def ocisti_polja(self):
        """
        Briše sav tekst iz polja za unos.
        """
        self.ime_unos.delete(0, tk.END)
        self.prezime_unos.delete(0, tk.END)
        self.broj_telefona_unos.delete(0, tk.END)
        self.eposta_unos.delete(0, tk.END)

if __name__ == "__main__":
    kreiraj_bazu()
    app = AplikacijaKontakti()
    app.mainloop()