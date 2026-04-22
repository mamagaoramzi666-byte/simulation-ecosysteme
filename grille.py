# grille.py
# La grille représente le terrain de notre écosystèmme
# C'est ici que les animaux vivent, bougent et interagissent

import random
from proie import Lapin
from predateur import Loup

class Grille:
    def __init__(self, largeur, hauteur):
        # La taille de notre terrain
        self.largeur = largeur
        self.hauteur = hauteur
        # Liste qui contient tous les animaux vivants
        self.animaux = []

    def ajouter_animal(self,animal):
        # On ajoute un animal à la grille
        self.animaux.apprend(animal)

    def placer_animaux_aleatoirement(self, nb_lapins, nb_loups):
        # On place les lapins au hasard sur la grille
        for _ in range(nb_lapins):
            x = random.randint(0, self.largeur - 1)
            y = random.randint(0, self.hauteur - 1)
            self.animaux.append(Loup(x, y))

        # On place les loups au hasard sur la grille
        for _ in range(nb_loups):
            x = random.randint(0, self.largeur - 1)
            y = random.randint(0, self.hauteur - 1)
            self.animaux.append(Loup(x, y))

        print(f" {nb_lapins} lapins et {nb_loups} loups placés sur la grille.")
    
    def deplacer_animal(self, animal):
        # L'animal se déplace d'une case au hasard
        # On calcule la nouvelle position sans sortir de la grille
        nouvelle_x = max(0, min(self.largeur - 1, animal.x + random.randint(-1, 1)))
        nouvelle_y = max(0, min(self.hauteur - 1, animal.y + random.randint(-1, 1)))
        animal.se_deplacer(nouvelle_x, nouvelle_y)

    def verifier_interactions(self):
        # On vérifie si un loup et un lapin sont sur la même case
        lapins = [a for a in self.animaux if isinstance(a, Lapin) and a.est_vivant()]
        loups  = [a for a in self.animaux if isinstance(a, Loup)  and a.est_vivant()]

        for loup in loups:
            for lapin in lapins:
                # Si le loup et le lapin sont sur la même case
                if loup.x == lapin.x and loup.y == lapin.y:
                    loup.chasser(lapin)

    def supprimer_morts(self):
        # On retire de la liste tous les animaux morts
        nb_avant = len(self.animaux)
        self.animaux = [a for a in self.animaux if a.est_vivant()]
        nb_apres = len(self.animaux)
        if nb_avant != nb_apres:
            print(f" {nb_avant - nb_apres} animal(aux) retiré(s) de la grille.")

    def afficher_stats(self):
        # On affiche le nombre de lapins et loups encore vivants
        nb_lapins = sum(1 for a in self.animaux if isinstance(a, Lapin))
        nb_loups  = sum(1 for a in self.animaux if isinstance(a, Loup))
        print(f" Lapins vivants : {nb_lapins} | Loups vivants : {nb_loups}")

    def afficher_grille(self):
        # On affiche une représentation visuelle de la grille dans le terminal
        print("\n" + "=" * (self.largeur * 2 + 1))
        for y in range(self.hauteur):
            ligne = "|"
            for x in range(self.largeur):
                # On cherche si un animal est sur cette case
                animal_ici = None
                for a in self.animaux:
                    if a.x == x and a.y == y and a.est_vivant():
                        animal_ici = a
                        break
                # On affiche L pour lapin, W pour loup, . pour vide
                if isinstance(animal_ici, Lapin):
                    ligne += "L|"
                elif isinstance(animal_ici, Loup):
                    ligne += "W|"
                else:
                    ligne += " |"
            print(ligne)
        print("=" * (self.largeur * 2 + 1) + "\n")

    def jouer_un_tour(self):
        # Tout ce qui se passe pendant un tour de simulation
        print("\n--- Nouveau tour ---")

        # 1. Chaque animal se déplace et passe un tour
        for animal in self.animaux:
            if animal.est_vivant():
                self.deplacer_animal(animal)
                animal.passer_un_tour()

                # 2. Si c'est un lapin, il mange de l'herbe
                if isinstance(animal, Lapin):
                    animal.manger()

        # 3. On vérifie les interactions (chasse)
        self.verifier_interactions()

        # 4. On retire les animaux morts
        self.supprimer_morts()

        # 5. On affiche les stats et la grille
        self.afficher_stats()
        self.afficher_grille()