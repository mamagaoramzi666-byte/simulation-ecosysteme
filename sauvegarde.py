# sauvegarde.py
# Gere la sauvegarde et le chargement de la simulation en JSON

import json
import os
from proie import Lapin
from predateur import Loup
from grille import Grille

FICHIER_SAUVEGARDE = "sauvegarde.json"

def sauvegarder(grille):
    # Verification que la grille est valide
    if not isinstance(grille, Grille):
        raise TypeError("L'objet a sauvegarder doit etre une instance de Grille.")

    animaux_data = []
    for animal in grille.animaux:
        if animal.est_vivant():
            animaux_data.append({
                "type"                  : "lapin" if isinstance(animal, Lapin) else "loup",
                "x"                     : animal.x,
                "y"                     : animal.y,
                "energie"               : animal.energie,
                "tours_sans_reproduire" : animal.tours_sans_reproduire
            })

    data = {
        "largeur" : grille.largeur,
        "hauteur" : grille.hauteur,
        "animaux" : animaux_data
    }

    try:
        with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Simulation sauvegardee dans '{FICHIER_SAUVEGARDE}'.")
    except IOError:
        print("Erreur : impossible d'ecrire le fichier de sauvegarde.")

def charger():
    # Verification que le fichier existe
    if not os.path.exists(FICHIER_SAUVEGARDE):
        print("Aucune sauvegarde trouvee.")
        return None

    try:
        with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Erreur : le fichier de sauvegarde est corrompu.")
        return None
    except IOError:
        print("Erreur : impossible de lire le fichier de sauvegarde.")
        return None

    # Verification que les cles necessaires sont presentes
    if "largeur" not in data or "hauteur" not in data or "animaux" not in data:
        print("Erreur : le fichier de sauvegarde est incomplet.")
        return None

    # On recrée la grille et les animaux
    grille = Grille(data["largeur"], data["hauteur"])

    for a in data["animaux"]:
        if a["type"] == "lapin":
            animal = Lapin(a["x"], a["y"])
        else:
            animal = Loup(a["x"], a["y"])

        animal.energie               = a["energie"]
        animal.tours_sans_reproduire = a["tours_sans_reproduire"]
        grille.ajouter_animal(animal)

    print(f"Sauvegarde chargee. ({len(grille.animaux)} animaux restaures)")
    return grille

def sauvegarde_existe():
    return os.path.exists(FICHIER_SAUVEGARDE)