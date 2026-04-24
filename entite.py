# entite.py
# Classe mere : tout etre vivant dans notre ecosysteme herite de cette classe

class EtreVivant:

    def __init__(self, x, y, energie):
        # Verification que les coordonnees sont des entiers
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Les coordonnees x et y doivent etre des entiers.")
        # Verification que l'energie est un nombre positif
        if not isinstance(energie, (int, float)) or energie <= 0:
            raise ValueError("L'energie doit etre un nombre positif.")

        self.x = x
        self.y = y
        self.energie = energie
        self.vivant = True

    def est_vivant(self):
        return self.vivant

    def perdre_energie(self, quantite):
        if quantite < 0:
            raise ValueError("La quantite d'energie perdue ne peut pas etre negative.")
        self.energie -= quantite
        if self.energie <= 0:
            self.vivant = False

    def se_deplacer(self, nouvelle_x, nouvelle_y):
        if not isinstance(nouvelle_x, int) or not isinstance(nouvelle_y, int):
            raise TypeError("Les nouvelles coordonnees doivent etre des entiers.")
        self.x = nouvelle_x
        self.y = nouvelle_y

    def __str__(self):
        return f"EtreVivant en ({self.x},{self.y}) | Energie: {self.energie}"