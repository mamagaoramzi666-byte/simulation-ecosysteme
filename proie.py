# proie.py
# Classe Lapin : herite de EtreVivant
# Le lapin mange de l'herbe et peut se reproduire

from entite import EtreVivant

class Lapin(EtreVivant):

    def __init__(self, x, y):
        # Un lapin commence avec 10 d'energie
        super().__init__(x, y, energie=10)
        self.tours_sans_reproduire = 0

    def manger(self):
        # Le lapin mange de l'herbe et gagne de l'energie
        self.energie += 4
        print(f"Le lapin en ({self.x},{self.y}) mange de l'herbe. Energie : {self.energie}")

    def peut_se_reproduire(self):
        # Le lapin peut se reproduire apres 3 tours
        return self.tours_sans_reproduire >= 3

    def se_reproduire(self):
        # Remise a zero du compteur apres reproduction
        if not self.est_vivant():
            raise Exception("Un lapin mort ne peut pas se reproduire.")
        self.tours_sans_reproduire = 0
        print(f"Le lapin en ({self.x},{self.y}) se reproduit.")

    def passer_un_tour(self):
        # Le lapin perd 1 energie et vieillit d'un tour
        if not self.est_vivant():
            raise Exception("Impossible de faire passer un tour a un animal mort.")
        self.perdre_energie(1)
        self.tours_sans_reproduire += 1

    def __str__(self):
        return f" Lapin en ({self.x},{self.y}) | Energie :{self.energie} | Vivant : {self.vivant}"