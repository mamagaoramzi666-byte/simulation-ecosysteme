# entitd.py
# classe mère: tout etre vivant dans notre écosystème hérite de cette classe
class EtreVivant:
    def __init__(self, x, y, energie):
        # La position de l'animal sur la grille (x= colonne, y= ligne) :
        self.x = x
        self.y = y
        # L'énergie de l'animal (quant elle tombe à 0, il meurt)
        self.energie = energie
        # L'animal est vivant au départ
        self.vivant = True

    def est_vivant(self):
        # Retourne True si l'animal est encore en vie
        return self.vivant    
    
    def perdre_energie(self, quantite):
        # L'animal perd de l'énergie à chaque tour
        self.energie -= quantite
        if self.energie <= 0:
            self.vivant = False # Il meurt si energie = 0

    def se_deplacer(self, nouvelle_x, nouvelle_y):
        # L'animal change de position sur la grille
        self.x = nouvelle_x
        self.y = nouvelle_y    
    def __str__(self):
        # Permet d'afficher l'animal proprement avec print()
        return f"EtreVivant en ({self.x}, {self.y}) | Energie: {self.energie}"