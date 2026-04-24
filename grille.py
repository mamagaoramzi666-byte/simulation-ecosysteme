# grille.py
# La grille represente le terrain de notre ecosysteme
# C'est ici que les animaux vivent, bougent et interagissent

import random
from proie import Lapin
from predateur import Loup

class Grille:

    def __init__(self, largeur, hauteur):
        # Verification que les dimensions sont valides
        if not isinstance(largeur, int) or not isinstance(hauteur, int):
            raise TypeError("La largeur et la hauteur doivent etre des entiers.")
        if largeur <= 0 or hauteur <= 0:
            raise ValueError("La largeur et la hauteur doivent etre positives.")

        self.largeur = largeur
        self.hauteur = hauteur
        self.animaux = []

    def ajouter_animal(self, animal):
        # Verification que l'animal est valide
        if not isinstance(animal, (Lapin, Loup)):
            raise TypeError("L'animal doit etre un Lapin ou un Loup.")
        self.animaux.append(animal)

    def placer_animaux_aleatoirement(self, nb_lapins, nb_loups):
        # Verification que les nombres sont valides
        if nb_lapins < 0 or nb_loups < 0:
            raise ValueError("Le nombre d'animaux ne peut pas etre negatif.")
        if nb_lapins + nb_loups > self.largeur * self.hauteur:
            raise ValueError("Trop d'animaux pour la taille de la grille.")

        cases_occupees = []

        for _ in range(nb_lapins):
            while True:
                x = random.randint(0, self.largeur - 1)
                y = random.randint(0, self.hauteur - 1)
                if (x, y) not in cases_occupees:
                    cases_occupees.append((x, y))
                    self.animaux.append(Lapin(x, y))
                    break

        for _ in range(nb_loups):
            while True:
                x = random.randint(0, self.largeur - 1)
                y = random.randint(0, self.hauteur - 1)
                if (x, y) not in cases_occupees:
                    cases_occupees.append((x, y))
                    self.animaux.append(Loup(x, y))
                    break

        print(f"5 lapins et {nb_loups} loups places sur la grille.")

    def deplacer_animal(self, animal):
        # Verification que l'animal est vivant avant de le deplacer
        if not animal.est_vivant():
            raise Exception("Impossible de deplacer un animal mort.")
        nouvelle_x = max(0, min(self.largeur - 1, animal.x + random.randint(-1, 1)))
        nouvelle_y = max(0, min(self.hauteur - 1, animal.y + random.randint(-1, 1)))
        animal.se_deplacer(nouvelle_x, nouvelle_y)

    def verifier_interactions(self):
        # On verifie si un loup et un lapin sont sur la meme case
        lapins = [a for a in self.animaux if isinstance(a, Lapin) and a.est_vivant()]
        loups  = [a for a in self.animaux if isinstance(a, Loup)  and a.est_vivant()]

        for loup in loups:
            for lapin in lapins:
                if loup.x == lapin.x and loup.y == lapin.y:
                    loup.chasser(lapin)

    def supprimer_morts(self):
        # On retire tous les animaux morts de la liste
        nb_avant = len(self.animaux)
        self.animaux = [a for a in self.animaux if a.est_vivant()]
        nb_apres = len(self.animaux)
        if nb_avant != nb_apres:
            print(f"{nb_avant - nb_apres} animal(aux) retire(s) de la grille.")

    def afficher_stats(self):
        # On affiche le nombre de lapins et loups encore vivants
        nb_lapins = sum(1 for a in self.animaux if isinstance(a, Lapin))
        nb_loups  = sum(1 for a in self.animaux if isinstance(a, Loup))
        print(f"Lapins vivants : {nb_lapins} | Loups vivants : {nb_loups}")

    def afficher_grille(self):
        # On affiche une representation visuelle de la grille dans le terminal
        print("\n" + "=" * (self.largeur * 2 + 1))
        for y in range(self.hauteur):
            ligne = "|"
            for x in range(self.largeur):
                animal_ici = None
                for a in self.animaux:
                    if a.x == x and a.y == y and a.est_vivant():
                        animal_ici = a
                        break
                if isinstance(animal_ici, Lapin):
                    ligne += "L|"
                elif isinstance(animal_ici, Loup):
                    ligne += "W|"
                else:
                    ligne += " |"
            print(ligne)
        print("=" * (self.largeur * 2 + 1) + "\n")

    def jouer_un_tour(self):
        print("\n--- Nouveau tour ---")

        for animal in self.animaux:
            if animal.est_vivant():
                self.deplacer_animal(animal)
                animal.passer_un_tour()
                if isinstance(animal, Lapin):
                    animal.manger()

        self.verifier_interactions()
        self.supprimer_morts()
        self.afficher_stats()
        self.afficher_grille()