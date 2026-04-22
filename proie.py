# proie.py
# Classe lapin mange de l'herbe et peut se reproduire

from entite import EtreVivant

class Lapin(EtreVivant):

    def __init__(self, x, y):
        # on appelle le constructeur de la classe mère
        # Un lapin commence avec 10 d'énergie 
        super().__init__(x, y, energie=10)
        # compteur de tours avant qu'il puisse se reproduire
        self.tours_sans_reproduire = 0

    def manger(self):
        # Le lapin mange de l'herbe : il gagne de l'énergie
        self.energie += 4
        print(f" Le lapin en ({self.x}, {self.y}) mange de l'herbe. Energie : {self.energie}")
    
    def peut_se_reproduire(self):
        # Le lapin peut se reproduire après 3 tours
        return self.tours_sans_reproduire >= 3
    
    def se_reproduire(self):
        # On remet le compteur à zéro après reproduction
        self.tours_sans_reproduire = 0
        print(f" Le lapin en ({self.x}, {self.y}) se reproduit !")
    
    def passer_un_tour(self):
        # A chaque tour, le lapin perd 1 énergie et vieillit
        self.perdre_energie(1)
        self.tours_sans_reproduire += 1
    
    def __str__(self):
        return f" Lapin en ({self.x}, {self.y}) | Energie :{self.energie} | Vivant : {self.vivant}"