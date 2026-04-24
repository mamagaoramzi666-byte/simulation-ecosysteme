# sauvegarde.py
# Gère la sauvegarde et le chargement de la simulation en JSON

import json
import os
from proie import Lapin
from predateur import Loup
from grille import Grille

# Nom du fichier de sauvegarde
FICHIER_SAUVEGARDE = "sauvegarde.json"

def sauvegarder(grille):
    # On transforme chaque animal en dictionnaire
    animaux_data = []
    for animal in grille.animaux:
        if animal.est_vivant():
            animaux_data.append({
                "type"    : "lapin" if isinstance(animal, Lapin) else "loup",
                "x"       : animal.x,
                "y"       : animal.y,
                "energie" : animal.energie,
                "tours_sans_reproduire" : animal.tours_sans_reproduire
            })

    # On crée le dictionnaire global de sauvegarde
    data = {
        "largeur" : grille.largeur,
        "hauteur" : grille.hauteur,
        "animaux" : animaux_data
    }

    # On écrit dans le fichier JSON
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n Simulation sauvegardée dans '{FICHIER_SAUVEGARDE}' !")

def charger():
    # On vérifie si le fichier existe
    if not os.path.exists(FICHIER_SAUVEGARDE):
        print(" Aucune sauvegarde trouvée.")
        return None

    # On lit le fichier JSON
    with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # On recrée la grille
    grille = Grille(data["largeur"], data["hauteur"])

    # On recrée chaque animal
    for a in data["animaux"]:
        if a["type"] == "lapin":
            animal = Lapin(a["x"], a["y"])
        else:
            animal = Loup(a["x"], a["y"])

        # On restaure l'énergie et le compteur
        animal.energie = a["energie"]
        animal.tours_sans_reproduire = a["tours_sans_reproduire"]
        grille.ajouter_animal(animal)

    print(f"\n Sauvegarde chargée ! ({len(grille.animaux)} animaux restaurés)")
    return grille

def sauvegarde_existe():
    return os.path.exists(FICHIER_SAUVEGARDE)