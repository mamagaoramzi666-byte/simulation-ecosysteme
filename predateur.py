# predateur.py
# classe Loup : hérite de EtreVivant
# Le loup chasse les lapins pour survivre

from entite import EtreVivant

class Loup(EtreVivant):

    def __init__(self, x, y):
        # Un loup commence avec 15 d'énergie(plus robuste que le lapin)
        super().__init__(x, y, energie=15)
        # compteur de tours avant qu'il puisse se reproduire
        self.tours_sans_reproduire = 0
    
    def chasser(self, lapin):
        # le loup mange un lapin : il gagne de l'énergie
        # et le lapin meurt
        if lapin.est_vivant():
            lapin.vivant = False
            self.energie += 8
            print(f" Le loup en ({self.x}, {self.y}) chasse le lapin en ({lapin.x}, {lapin.y}) !")
            print(f" Energie du loup après chasse : {self.energie}")
        else:
            print(f" Le loup essaie de chasser mais le lapin est déjà mort.")
    def peut_se_reproduire(self):
        # Le loup peut se reproduire après 5 tours
        return self.tours_sans_reproduire >=5
    
    def se_reproduire(self):
        # On remet le compteur à zéro après reproduction
        self.tours_sans_reproduire = 0
        print(f" Le loup en ({self.x}, {self.y}) se reproduit !")
    
    def passer_un_tour(self):
        # A chaque tour, le loup perd 2 énergie (il consomme plus)
        self.perdre_energie(2)
        self.tours_sans_reproduire += 1
    
    def __str__(self):
        return f" Loup en ({self.x}, {self.y}) | Energie : { self.energie} | Vivant : {self.vivant}" 
        