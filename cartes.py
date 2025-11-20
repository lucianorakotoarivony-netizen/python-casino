# cartes.py
import random
from enum import Enum
from typing import Tuple, List

class Couleur(Enum):
    """Les 4 couleurs d'un jeu de cartes"""
    COEUR: str = "♥"
    CARREAU: str = "♦" 
    TREFLE: str = "♣"
    PIQUE: str = "♠"
    
    def __str__(self) -> str:
        return self.value

class Valeur(Enum):
    """Les 13 valeurs avec leurs points au Blackjack"""
    AS: Tuple[int, int] = (1, 11)      # As peut valoir 1 ou 11
    DEUX: Tuple[int] = (2,)
    TROIS: Tuple[int] = (3,)
    QUATRE: Tuple[int] = (4,)
    CINQ: Tuple[int] = (5,)
    SIX: Tuple[int] = (6,)
    SEPT: Tuple[int] = (7,)
    HUIT: Tuple[int] = (8,)
    NEUF: Tuple[int] = (9,)
    DIX: Tuple[int] = (10,)
    VALET: Tuple[int] = (10,)
    DAME: Tuple[int] = (10,)
    ROI: Tuple[int] = (10,)
    
    def __str__(self) -> str:
        noms: dict[str, str] = {'AS': 'A', 'VALET': 'J', 'DAME': 'Q', 'ROI': 'K'}
        return noms.get(self.name, self.name.capitalize())
    
    def valeurs_possibles(self) -> Tuple[int, ...]:
        """Retourne les valeurs possibles de la carte"""
        return self.value

    def valeur_min(self) -> int:
        """Retourne la valeur minimale de la carte"""
        return self.value[0]

class Pack() :
    """Ensemble qui contient les jeux qui se joue avec une main"""
    def __init__(self) -> None:
        pass

class CarteJeu():
    def __init__(self, valeur : Valeur, couleur : Couleur) -> None:
        self.valeur : Valeur = valeur
        self.couleur : Couleur = couleur
        
    def __str__(self) -> str:
        return f"{self.valeur} {self.couleur}"
    
    def valeurs_possibles(self) -> Tuple[int, ...]:
        return self.valeur.value

class Pack52(Pack) :
    def __init__(self) -> None:
        self.cartes: list[CarteJeu] = []
        
    def initialisation(self) -> None:
        self.cartes = [
            CarteJeu(valeur, couleur) 
            for valeur in Valeur 
            for couleur in Couleur
        ]

class Hand() :
    def __init__(self) -> None:
        self.pieces: list[CarteJeu] = []
        
    def display(self) -> None:
        print("Main :", " | ".join(str(piece) for piece in self.pieces))
        
    def shuffle(self) -> None:
        random.shuffle(self.pieces)
        
    def add(self, carte: CarteJeu) -> None:
        """Ajoute une carte à la main"""
        self.pieces.append(carte)
        
    def empty(self) -> None:
        """Vide la main pour une nouvelle partie"""
        self.pieces.clear()