from player import Player
import time
import random
from copy import copy

class AIPlayerRandom(Player):

    def __init__(self):
        super(AIPlayerRandom, self).__init__()

    def getColumn(self, model):
        """Methode qui retourne la colonne à jouer"""
        while True:
            index = random.randint(0,6)
            if model[index][-1]==0:
                return index
        #on ne devrait pas arriver ici

class AIPlayerDebutantAA(Player):

    def __init__(self):
        super(AIPlayerDebutantAA, self).__init__()


    def getColumn(self, model):
        """Methode qui retourne la colonne générant l'heuristique à court terme
        (profondeur = 1) la plus élevée"""
        best_col = -1
        best_heuristic = - 1000
        for i in range(7):
            # on vérifie si la colonne est dispo
            if model[i][-1] == 0:
                row = 0
                # on cherche la première ligne vide
                while (row < len(model[i]) and model[i][row] != 0) :
                    row+=1
                # on ajoute un jeton
                model[i][row] = self.color
                # on calcule l'heuristique de ce nuveau modele
                temp_heuristic = self.heuristic(model)
                # on vérifie si la colonne est meilleure
                if (temp_heuristic > best_heuristic) :
                    best_col = i
                    best_heuristic = temp_heuristic
                # on reset le modele
                model[i][row] = 0
        return best_col



    def heuristic(self, grille):
        """Méthode qui calcule l'heuristique d'un modèle donné"""
        somme = 0
        # colonnes
        for i in range(7):  #colonnes
            for j in range(3):  #lignes
                zone =[grille[i][j], grille[i][j+1], grille[i][j+2], grille[i][j+3]]
                if not((-1) * self.color in zone) :
                    somme += zone.count(self.color)
                if not (self.color in zone) :
                    somme -= zone.count((-1) * self.color)
        # lignes
        for i in range(6):     #lignes
            for j in range(4):  #colonnes
                zone = [grille[j][i], grille[j+1][i], grille[j+2][i], grille[j+3][i]]
                if not((-1) * self.color in zone) :
                    if zone.count(self.color) == 4:
                        somme += 1000
                    else :
                        somme += zone.count(self.color)
                if not (self.color in zone) :
                    somme -= zone.count((-1) * self.color)
        # diagonales haut-droites
        for i in range(3):
            for j in range(4):
                zone = [grille[j][i+3], grille[j+1][i+2], grille[j+2][i+1], grille[j+3][i]]
                if not((-1) * self.color in zone) :
                    if zone.count(self.color) == 4:
                        somme += 1000
                    else :
                        somme += zone.count(self.color)
                if not (self.color in zone) :
                    somme -= zone.count((-1) * self.color)

        # diagonales haut-gauches
        for i in range(3):
            for j in range(4):
                zone = [grille[j+3][i+3], grille[j+2][i+2], grille[j+1][i+1], grille[j][i]]
                if not((-1) * self.color in zone) :
                    if zone.count(self.color) == 4:
                        somme += 1000
                    else :
                        somme += zone.count(self.color)
                if not (self.color in zone) :
                    somme -= zone.count((-1) * self.color)

        return somme
