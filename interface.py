# interface.py
# Interface graphique du simulateur d'ecosysteme
# Utilisation de Tkinter

import tkinter as tk
from tkinter import messagebox
from grille import Grille
from proie import Lapin
from predateur import Loup
from sauvegarde import sauvegarder, charger, sauvegarde_existe

# Dimensions de la fenetre
TAILLE_CASE = 50
COULEUR_FOND       = "#f0f0f0"
COULEUR_GRILLE     = "#cccccc"
COULEUR_LAPIN      = "#4CAF50"
COULEUR_LOUP       = "#f44336"
COULEUR_VIDE       = "#ffffff"
COULEUR_TEXTE      = "#333333"

class Interface:

    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Simulateur d'Ecosysteme")
        self.fenetre.configure(bg=COULEUR_FOND)
        self.grille  = None
        self.tour    = 0
        self.nb_tours = 0

        # On construit l'interface
        self.construire_menu()
        self.construire_canvas()
        self.construire_stats()
        self.construire_controles()

    def construire_menu(self):
        # Barre de menu en haut
        self.frame_menu = tk.Frame(self.fenetre, bg=COULEUR_FOND, pady=10)
        self.frame_menu.pack()

        tk.Label(
            self.frame_menu,
            text="Simulateur d'Ecosysteme",
            font=("Arial", 16, "bold"),
            bg=COULEUR_FOND,
            fg=COULEUR_TEXTE
        ).pack()

    def construire_canvas(self):
        # Zone d'affichage de la grille
        self.frame_canvas = tk.Frame(self.fenetre, bg=COULEUR_FOND)
        self.frame_canvas.pack(padx=10)

        self.canvas = tk.Canvas(
            self.frame_canvas,
            width=10 * TAILLE_CASE,
            height=10 * TAILLE_CASE,
            bg=COULEUR_VIDE
        )
        self.canvas.pack()

    def construire_stats(self):
        # Zone d'affichage des statistiques
        self.frame_stats = tk.Frame(self.fenetre, bg=COULEUR_FOND, pady=5)
        self.frame_stats.pack()

        self.label_tour = tk.Label(
            self.frame_stats,
            text="Tour : 0",
            font=("Arial", 11),
            bg=COULEUR_FOND,
            fg=COULEUR_TEXTE
        )
        self.label_tour.grid(row=0, column=0, padx=20)

        self.label_lapins = tk.Label(
            self.frame_stats,
            text="Lapins : 0",
            font=("Arial", 11),
            bg=COULEUR_FOND,
            fg="#4CAF50"
        )
        self.label_lapins.grid(row=0, column=1, padx=20)

        self.label_loups = tk.Label(
            self.frame_stats,
            text="Loups : 0",
            font=("Arial", 11),
            bg=COULEUR_FOND,
            fg="#f44336"
        )
        self.label_loups.grid(row=0, column=2, padx=20)

    def construire_controles(self):
        # Zone des boutons de controle
        self.frame_controles = tk.Frame(self.fenetre, bg=COULEUR_FOND, pady=10)
        self.frame_controles.pack()

        # Champs de configuration
        tk.Label(self.frame_controles, text="Lapins :", bg=COULEUR_FOND).grid(row=0, column=0)
        self.entry_lapins = tk.Entry(self.frame_controles, width=5)
        self.entry_lapins.insert(0, "10")
        self.entry_lapins.grid(row=0, column=1, padx=5)

        tk.Label(self.frame_controles, text="Loups :", bg=COULEUR_FOND).grid(row=0, column=2)
        self.entry_loups = tk.Entry(self.frame_controles, width=5)
        self.entry_loups.insert(0, "3")
        self.entry_loups.grid(row=0, column=3, padx=5)

        tk.Label(self.frame_controles, text="Tours :", bg=COULEUR_FOND).grid(row=0, column=4)
        self.entry_tours = tk.Entry(self.frame_controles, width=5)
        self.entry_tours.insert(0, "20")
        self.entry_tours.grid(row=0, column=5, padx=5)

        # Boutons
        self.frame_boutons = tk.Frame(self.fenetre, bg=COULEUR_FOND, pady=5)
        self.frame_boutons.pack()

        tk.Button(
            self.frame_boutons,
            text="Nouvelle simulation",
            command=self.nouvelle_simulation,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            self.frame_boutons,
            text="Jouer un tour",
            command=self.jouer_tour,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            self.frame_boutons,
            text="Sauvegarder",
            command=self.sauvegarder,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            self.frame_boutons,
            text="Charger",
            command=self.charger,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18
        ).grid(row=0, column=3, padx=5)

    def nouvelle_simulation(self):
        # On demarre une nouvelle simulation avec les parametres entres
        try:
            nb_lapins = int(self.entry_lapins.get())
            nb_loups  = int(self.entry_loups.get())
            nb_tours  = int(self.entry_tours.get())

            if nb_lapins <= 0 or nb_loups <= 0 or nb_tours <= 0:
                messagebox.showerror("Erreur", "Les valeurs doivent etre positives.")
                return

            self.grille   = Grille(10, 10)
            self.tour     = 0
            self.nb_tours = nb_tours
            self.grille.placer_animaux_aleatoirement(nb_lapins, nb_loups)
            self.mettre_a_jour_affichage()

        except ValueError:
            messagebox.showerror("Erreur", "Entrez des nombres entiers valides.")

    def jouer_tour(self):
        # On joue un tour de simulation
        if self.grille is None:
            messagebox.showwarning("Attention", "Lancez d'abord une nouvelle simulation.")
            return

        if self.tour >= self.nb_tours:
            messagebox.showinfo("Fin", "La simulation est terminee.")
            return

        if len(self.grille.animaux) == 0:
            messagebox.showinfo("Fin", "Tous les animaux sont morts.")
            return

        self.grille.jouer_un_tour()
        self.tour += 1
        self.mettre_a_jour_affichage()

        if len(self.grille.animaux) == 0:
            messagebox.showinfo("Fin", "Tous les animaux sont morts.")

    def sauvegarder(self):
        # On sauvegarde la simulation en cours
        if self.grille is None:
            messagebox.showwarning("Attention", "Aucune simulation en cours.")
            return
        sauvegarder(self.grille)
        messagebox.showinfo("Sauvegarde", "Simulation sauvegardee avec succes.")

    def charger(self):
        # On charge une simulation sauvegardee
        if not sauvegarde_existe():
            messagebox.showwarning("Attention", "Aucune sauvegarde trouvee.")
            return
        self.grille = charger()
        self.tour   = 0
        self.mettre_a_jour_affichage()

    def mettre_a_jour_affichage(self):
        # On redessine la grille et on met a jour les stats
        self.canvas.delete("all")

        for y in range(10):
            for x in range(10):
                x1 = x * TAILLE_CASE
                y1 = y * TAILLE_CASE
                x2 = x1 + TAILLE_CASE
                y2 = y1 + TAILLE_CASE

                # On cherche si un animal est sur cette case
                animal_ici = None
                for a in self.grille.animaux:
                    if a.x == x and a.y == y and a.est_vivant():
                        animal_ici = a
                        break

                # On colorie la case selon l'animal
                if isinstance(animal_ici, Lapin):
                    couleur = COULEUR_LAPIN
                    lettre  = "L"
                elif isinstance(animal_ici, Loup):
                    couleur = COULEUR_LOUP
                    lettre  = "W"
                else:
                    couleur = COULEUR_VIDE
                    lettre  = ""

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline=COULEUR_GRILLE)

                if lettre:
                    self.canvas.create_text(
                        x1 + TAILLE_CASE // 2,
                        y1 + TAILLE_CASE // 2,
                        text=lettre,
                        font=("Arial", 14, "bold"),
                        fill="white"
                    )

        # On met a jour les stats
        nb_lapins = sum(1 for a in self.grille.animaux if isinstance(a, Lapin))
        nb_loups  = sum(1 for a in self.grille.animaux if isinstance(a, Loup))

        self.label_tour.config(text=f"Tour : {self.tour}/{self.nb_tours}")
        self.label_lapins.config(text=f"Lapins : {nb_lapins}")
        self.label_loups.config(text=f"Loups : {nb_loups}")

# Point d'entree
if __name__ == "__main__":
    fenetre = tk.Tk()
    fenetre.geometry("600x700")
    fenetre.resizable(True, True)
    app = Interface(fenetre)
    fenetre.mainloop()