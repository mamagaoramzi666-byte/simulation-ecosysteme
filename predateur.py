# predateur.py
# Classe Loup : herite de EtreVivant
# Le loup chasse les lapins pour survivre

from entite import EtreVivant

class Loup(EtreVivant):

    def __init__(self, x, y):
        # Un loup commence avec 15 d'energie
        super().__init__(x, y, energie=15)
        self.tours_sans_reproduire = 0

    def chasser(self, lapin):
        # Verification que la cible est bien un animal valide
        if lapin is None:
            raise TypeError("La cible de la chasse ne peut pas etre vide.")
        if not lapin.est_vivant():
            print(f"Le loup en ({self.x},{self.y}) essaie de chasser mais le lapin est deja mort.")
            return
        # Le loup mange le lapin et gagne de l'energie
        lapin.vivant = False
        self.energie += 8
        print(f"Le loup en ({self.x},{self.y}) chasse le lapin en ({lapin.x},{lapin.y}).")
        print(f"Energie du loup apres chasse : {self.energie}")

    def peut_se_reproduire(self):
        # Le loup peut se reproduire apres 5 tours
        return self.tours_sans_reproduire >= 5

    def se_reproduire(self):
        # Remise a zero du compteur apres reproduction
        if not self.est_vivant():
            raise Exception("Un loup mort ne peut pas se reproduire.")
        self.tours_sans_reproduire = 0
        print(f"Le loup en ({self.x},{self.y}) se reproduit.")

    def passer_un_tour(self):
        # Le loup perd 2 energie par tour
        if not self.est_vivant():
            raise Exception("Impossible de faire passer un tour a un animal mort.")
        self.perdre_energie(2)
        self.tours_sans_reproduire += 1

    def __str__(self):
        return f" Loup en ({self.x},{self.y}) | Energie : {self.energie} | Vivant : {self.vivant}"