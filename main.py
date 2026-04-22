# main.py
# Version interactive - L'utilisateur contrôle un animal

from grille import Grille
from proie import Lapin
from predateur import Loup

def choisir_animal(grille):
    # On liste tous les animaux vivants avec leur numéro
    print("\n Choisissez votre animal :")
    animaux_vivants = [a for a in grille.animaux if a.est_vivant()]

    for i, animal in enumerate(animaux_vivants):
        print(f"  [{i}] {animal}")

    while True:
        try:
            choix = int(input("\nEntrez le numéro de l'animal : "))
            if 0 <= choix < len(animaux_vivants):
                return animaux_vivants[choix]
            else:
                print("❌ Numéro invalide, réessaie.")
        except ValueError:
            print("❌ Entre un chiffre valide.")

def deplacer_manuellement(animal, grille):
    # L'utilisateur choisit la direction de déplacement
    print("\n Dans quelle direction voulez-vous aller ?")
    print("  [z] Haut")
    print("  [s] Bas")
    print("  [q] Gauche")
    print("  [d] Droite")
    print("  [x] Rester sur place")

    direction = input("\nVotre choix : ").strip().lower()

    # On calcule la nouvelle position selon la direction
    nouvelle_x = animal.x
    nouvelle_y = animal.y

    if direction == "z":
        nouvelle_y = max(0, animal.y - 1)
    elif direction == "s":
        nouvelle_y = min(grille.hauteur - 1, animal.y + 1)
    elif direction == "q":
        nouvelle_x = max(0, animal.x - 1)
    elif direction == "d":
        nouvelle_x = min(grille.largeur - 1, animal.x + 1)
    elif direction == "x":
        print("  L'animal reste sur place.")
    else:
        print("Direction invalide, l'animal reste sur place.")

    animal.se_deplacer(nouvelle_x, nouvelle_y)
    print(f" Animal déplacé en ({animal.x}, {animal.y})")

def menu_principal():
    print("=" * 40)
    print("   SIMULATEUR D'ÉCOSYSTÈME ")
    print("   Proies & Prédateurs — L2 Info")
    print("=" * 40)

    # L'utilisateur choisit le nombre d'animaux
    print("\n Configuration de la simulation :")
    while True:
        try:
            nb_lapins = int(input("Nombre de lapins : "))
            nb_loups = int(input("Nombre de loups  : "))
            nb_tours = int(input("Nombre de tours  : "))
            break
        except ValueError:
            print("Entre des chiffres valides.")

    # On crée la grille et on place les animaux
    grille = Grille(largeur=10, hauteur=10)
    grille.placer_animaux_aleatoirement(nb_lapins, nb_loups)

    print("\n État initial :")
    grille.afficher_stats()
    grille.afficher_grille()

    # Boucle principale de la simulation
    for tour in range(1, nb_tours + 1):
        print(f"\n{'=' * 40}")
        print(f" TOUR {tour}/{nb_tours}")
        print(f"{'=' * 40}")

        if len(grille.animaux) == 0:
            print("\n Tous les animaux sont morts. Fin de simulation.")
            break

        # L'utilisateur choisit un animal à contrôler
        animal_choisi = choisir_animal(grille)
        print(f"\n Vous contrôlez : {animal_choisi}")

        # L'utilisateur déplace son animal
        deplacer_manuellement(animal_choisi, grille)

        # Les autres animaux bougent automatiquement
        print("\n Les autres animaux bougent automatiquement...")
        for animal in grille.animaux:
            if animal.est_vivant() and animal != animal_choisi:
                grille.deplacer_animal(animal)
                animal.passer_un_tour()
                if isinstance(animal, Lapin):
                    animal.manger()

        # L'animal contrôlé passe aussi son tour
        animal_choisi.passer_un_tour()
        if isinstance(animal_choisi, Lapin):
            animal_choisi.manger()

        # On vérifie les interactions et on nettoie
        grille.verifier_interactions()
        grille.supprimer_morts()

        # On affiche l'état après le tour
        grille.afficher_stats()
        grille.afficher_grille()

    # Fin de la simulation
    print("\n" + "=" * 40)
    print(" Simulation terminée !")
    print("=" * 40)
    grille.afficher_stats()

if __name__ == "__main__":
    menu_principal()