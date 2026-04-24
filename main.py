# main.py
# Version avec sauvegarde JSON - Bloc 4

from grille import Grille
from proie import Lapin
from predateur import Loup
from sauvegarde import sauvegarder, charger, sauvegarde_existe

def choisir_animal(grille):
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
    print("\n  Dans quelle direction voulez-vous aller ?")
    print("  [z] Haut")
    print("  [s] Bas")
    print("  [q] Gauche")
    print("  [d] Droite")
    print("  [x] Rester sur place")

    direction = input("\nVotre choix : ").strip().lower()

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
        print(" Direction invalide, l'animal reste sur place.")

    animal.se_deplacer(nouvelle_x, nouvelle_y)
    print(f" Animal déplacé en ({animal.x}, {animal.y})")

def configurer_nouvelle_partie():
    # L'utilisateur configure une nouvelle simulation
    print("\n  Configuration de la simulation :")
    while True:
        try:
            nb_lapins = int(input("Nombre de lapins : "))
            nb_loups  = int(input("Nombre de loups  : "))
            nb_tours  = int(input("Nombre de tours  : "))
            break
        except ValueError:
            print(" Entre des chiffres valides.")

    grille = Grille(largeur=10, hauteur=10)
    grille.placer_animaux_aleatoirement(nb_lapins, nb_loups)
    return grille, nb_tours

def menu_demarrage():
    # Menu affiché au lancement du programme
    print("=" * 40)
    print("    SIMULATEUR D'ÉCOSYSTÈME ")
    print("   Proies & Prédateurs — L2 Info")
    print("=" * 40)

    print("\n Menu principal :")
    print("  [1] Nouvelle simulation")

    # On affiche l'option charger seulement si une save existe
    if sauvegarde_existe():
        print("  [2] Charger la dernière sauvegarde")
        print("  [3] Quitter")
        choix_valides = ["1", "2", "3"]
    else:
        print("  [2] Quitter")
        choix_valides = ["1", "2"]

    while True:
        choix = input("\nVotre choix : ").strip()
        if choix in choix_valides:
            return choix
        print(" Choix invalide, réessaie.")

def menu_en_jeu():
    # Menu affiché à chaque tour
    print("\n Que voulez-vous faire ?")
    print("  [1] Jouer le tour suivant")
    print("  [2] Sauvegarder et continuer")
    print("  [3] Sauvegarder et quitter")
    print("  [4] Quitter sans sauvegarder")

    while True:
        choix = input("\nVotre choix : ").strip()
        if choix in ["1", "2", "3", "4"]:
            return choix
        print(" Choix invalide, réessaie.")

def jouer_tour(grille, tour, nb_tours):
    print(f"\n{'=' * 40}")
    print(f"    TOUR {tour}/{nb_tours}")
    print(f"{'=' * 40}")

    if len(grille.animaux) == 0:
        print("\n Tous les animaux sont morts. Fin de simulation.")
        return False

    # L'utilisateur choisit et déplace son animal
    animal_choisi = choisir_animal(grille)
    print(f"\n✅ Vous contrôlez : {animal_choisi}")
    deplacer_manuellement(animal_choisi, grille)

    # Les autres animaux bougent automatiquement
    print("\n Les autres animaux bougent automatiquement...")
    for animal in grille.animaux:
        if animal.est_vivant() and animal != animal_choisi:
            grille.deplacer_animal(animal)
            animal.passer_un_tour()
            if isinstance(animal, Lapin):
                animal.manger()

    # L'animal contrôlé passe son tour
    animal_choisi.passer_un_tour()
    if isinstance(animal_choisi, Lapin):
        animal_choisi.manger()

    # Interactions et nettoyage
    grille.verifier_interactions()
    grille.supprimer_morts()

    # Affichage
    grille.afficher_stats()
    grille.afficher_grille()
    return True

def menu_principal():
    choix = menu_demarrage()

    # Nouvelle partie
    if choix == "1":
        grille, nb_tours = configurer_nouvelle_partie()

    # Charger sauvegarde
    elif choix == "2" and sauvegarde_existe():
        grille = charger()
        if grille is None:
            return
        nb_tours = int(input("Combien de tours voulez-vous jouer ? "))

    # Quitter
    else:
        print("\n À bientôt !")
        return

    # Affichage état initial
    print("\n État initial :")
    grille.afficher_stats()
    grille.afficher_grille()

    # Boucle principale
    for tour in range(1, nb_tours + 1):

        # Menu en jeu
        action = menu_en_jeu()

        if action == "1":
            # Jouer le tour
            continuer = jouer_tour(grille, tour, nb_tours)
            if not continuer:
                break

        elif action == "2":
            # Sauvegarder et continuer
            sauvegarder(grille)
            continuer = jouer_tour(grille, tour, nb_tours)
            if not continuer:
                break

        elif action == "3":
            # Sauvegarder et quitter
            sauvegarder(grille)
            print("\n Simulation sauvegardée. À bientôt !")
            return

        elif action == "4":
            # Quitter sans sauvegarder
            print("\n Simulation abandonnée sans sauvegarde.")
            return

    # Fin normale
    print("\n" + "=" * 40)
    print("    Simulation terminée !")
    print("=" * 40)
    grille.afficher_stats()

    # Proposer de sauvegarder à la fin
    print("\n Voulez-vous sauvegarder cette partie ?")
    print("  [1] Oui")
    print("  [2] Non")
    if input("Votre choix : ").strip() == "1":
        sauvegarder(grille)

if __name__ == "__main__":
    menu_principal()