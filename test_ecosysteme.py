# test_ecosysteme.py
# Tests unitaires du simulateur d'ecosysteme
# Utilisation : pytest test_ecosysteme.py

import pytest
from entite import EtreVivant
from proie import Lapin
from predateur import Loup
from grille import Grille

# ============================================================
# TESTS DE LA CLASSE EtreVivant
# ============================================================

def test_creation_etre_vivant():
    # On verifie qu'un etre vivant est bien cree avec les bons attributs
    e = EtreVivant(2, 3, 10)
    assert e.x == 2
    assert e.y == 3
    assert e.energie == 10
    assert e.vivant == True

def test_coordonnees_invalides():
    # On verifie qu'une erreur est levee si les coordonnees ne sont pas des entiers
    with pytest.raises(TypeError):
        EtreVivant("a", 3, 10)

def test_energie_invalide():
    # On verifie qu'une erreur est levee si l'energie est negative ou nulle
    with pytest.raises(ValueError):
        EtreVivant(0, 0, -5)

def test_perdre_energie():
    # On verifie que l'animal perd bien de l'energie
    e = EtreVivant(0, 0, 10)
    e.perdre_energie(4)
    assert e.energie == 6
    assert e.vivant == True

def test_mort_quand_energie_nulle():
    # On verifie que l'animal meurt quand son energie tombe a zero
    e = EtreVivant(0, 0, 5)
    e.perdre_energie(5)
    assert e.vivant == False

def test_se_deplacer():
    # On verifie que l'animal change bien de position
    e = EtreVivant(0, 0, 10)
    e.se_deplacer(3, 4)
    assert e.x == 3
    assert e.y == 4

# ============================================================
# TESTS DE LA CLASSE Lapin
# ============================================================

def test_creation_lapin():
    # On verifie qu'un lapin est bien cree avec 10 d'energie
    lapin = Lapin(1, 1)
    assert lapin.energie == 10
    assert lapin.vivant == True
    assert lapin.tours_sans_reproduire == 0

def test_lapin_manger():
    # On verifie que le lapin gagne de l'energie en mangeant
    lapin = Lapin(0, 0)
    lapin.manger()
    assert lapin.energie == 14

def test_lapin_passer_un_tour():
    # On verifie que le lapin perd 1 energie par tour
    lapin = Lapin(0, 0)
    lapin.passer_un_tour()
    assert lapin.energie == 9
    assert lapin.tours_sans_reproduire == 1

def test_lapin_peut_se_reproduire():
    # On verifie que le lapin peut se reproduire apres 3 tours
    lapin = Lapin(0, 0)
    lapin.tours_sans_reproduire = 3
    assert lapin.peut_se_reproduire() == True

def test_lapin_ne_peut_pas_se_reproduire():
    # On verifie que le lapin ne peut pas se reproduire avant 3 tours
    lapin = Lapin(0, 0)
    lapin.tours_sans_reproduire = 1
    assert lapin.peut_se_reproduire() == False

# ============================================================
# TESTS DE LA CLASSE Loup
# ============================================================

def test_creation_loup():
    # On verifie qu'un loup est bien cree avec 15 d'energie
    loup = Loup(2, 2)
    assert loup.energie == 15
    assert loup.vivant == True
    assert loup.tours_sans_reproduire == 0

def test_loup_chasser():
    # On verifie que le loup mange un lapin et gagne de l'energie
    loup  = Loup(3, 3)
    lapin = Lapin(3, 3)
    loup.chasser(lapin)
    assert lapin.vivant == False
    assert loup.energie == 23

def test_loup_chasser_lapin_mort():
    # On verifie que le loup ne peut pas chasser un lapin deja mort
    loup        = Loup(0, 0)
    lapin       = Lapin(0, 0)
    lapin.vivant = False
    energie_avant = loup.energie
    loup.chasser(lapin)
    assert loup.energie == energie_avant

def test_loup_passer_un_tour():
    # On verifie que le loup perd 2 energie par tour
    loup = Loup(0, 0)
    loup.passer_un_tour()
    assert loup.energie == 13
    assert loup.tours_sans_reproduire == 1

def test_loup_peut_se_reproduire():
    # On verifie que le loup peut se reproduire apres 5 tours
    loup = Loup(0, 0)
    loup.tours_sans_reproduire = 5
    assert loup.peut_se_reproduire() == True

# ============================================================
# TESTS DE LA CLASSE Grille
# ============================================================

def test_creation_grille():
    # On verifie qu'une grille est bien creee avec les bonnes dimensions
    grille = Grille(10, 10)
    assert grille.largeur == 10
    assert grille.hauteur == 10
    assert len(grille.animaux) == 0

def test_grille_dimensions_invalides():
    # On verifie qu'une erreur est levee si les dimensions sont invalides
    with pytest.raises(ValueError):
        Grille(0, 10)

def test_ajouter_animal():
    # On verifie qu'on peut ajouter un animal a la grille
    grille = Grille(10, 10)
    lapin  = Lapin(0, 0)
    grille.ajouter_animal(lapin)
    assert len(grille.animaux) == 1

def test_placer_animaux_aleatoirement():
    # On verifie que le bon nombre d'animaux est place sur la grille
    grille = Grille(10, 10)
    grille.placer_animaux_aleatoirement(5, 3)
    assert len(grille.animaux) == 8

def test_supprimer_morts():
    # On verifie que les animaux morts sont bien retires de la grille
    grille      = Grille(10, 10)
    lapin       = Lapin(0, 0)
    lapin.vivant = False
    grille.ajouter_animal(lapin)
    grille.supprimer_morts()
    assert len(grille.animaux) == 0

def test_verifier_interactions():
    # On verifie qu'un loup mange un lapin sur la meme case
    grille = Grille(10, 10)
    lapin  = Lapin(5, 5)
    loup   = Loup(5, 5)
    grille.ajouter_animal(lapin)
    grille.ajouter_animal(loup)
    grille.verifier_interactions()
    assert lapin.vivant == False