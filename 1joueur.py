import pygame
import sys
import time
import random as rd
import numpy as np
from math import inf

#Imports, initialisation
pygame.init ()
image = pygame.image.load ("Grille.png")
size = image.get_size ()
screen = pygame.display.set_mode (size)
screen.blit (image, (0,0))
pygame.display.flip ()

pionjaune = pygame.image.load ("PionJaune.png")
pionrouge = pygame.image.load ("PionRouge.png")
font = pygame.font.Font ("freesansbold.ttf", 15)

# Données globales
 
M = [[0, 0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0, 0], \
     [0, 0, 0, 0, 0, 0, 0]]
 
joueur = 1
JetonsJoues = 0
P4 = False

# Affichage
def affichage(matrice):
    screen.fill((0,0,0))
    screen.blit(image,(0,0))
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j]==1:
                screen.blit(pionrouge,(16+97*j,13-97.5*i+486))
                pygame.display.flip()
            if matrice[i][j]==2:
                screen.blit(pionjaune,(16+97*j,13-97.5*i+486))
                pygame.display.flip()


# Fonctions utiles 
def quel_joueur():
# Cette fonction retourne le numero du joueur qui doit jouer
    if (JetonsJoues % 2 == 0):
        jou = 1
    else:
        jou = 2
    return jou

def choisir_colonne(x,y):
    '''Cette fonction retourne la colonne demandee par le joueur 1 suivant où il a cliqué'''
    col=x-16
    col=int(col/97)
    return verif_colonne(col)

def verif_colonne(col):
    '''vérifie si la colonne est valable, sinon, renvoie la première colonne à droite disponble'''
    while M[5][col] != 0:
        col = (col+1)%7
    return col

def colonne_disponible(M,col):
    '''retourne vrai ou faux suivant si la colonne est disponible'''
    return (M[5][col] == 0)
     
def ligne(colonne):
# Cette fonction retourne la ligne vide correspondant a la colonne demandee
    lig = 0
    for i in range (1,6):
        if ( M[i][colonne] == 0 and M[i-1][colonne] != 0 ):
            lig = i
    return lig

def verification_P4():
    '''teste si un joueur a gagné ou pas, renvoie le numéro du joueur le cas échéant'''
    vainqueur = 0
    for joueur in [2,1]:
        #teste toutes les possibilités en lignes
        for i in range(6):
            for j in range(4):
                if M[i][j] == joueur and M[i][j+1] == joueur and M[i][j+2] == joueur and M[i][j+3] == joueur:
                    vainqueur = joueur

        #teste toutes les possibilités en colonnes
        for j in range(7):
            for i in range(3):
                if M[i][j] == joueur and M[i+1][j] == joueur and M[i+2][j] == joueur and M[i+3][j] == joueur:
                    vainqueur = joueur
            
        #teste toutes les possibilités en diagonales montantes / et descendantes \
        for i in range(3):
            for j in range(4):
                if M[i][j] == joueur and M[i+1][j+1] == joueur and M[i+2][j+2] == joueur and M[i+3][j+3] == joueur:
                    vainqueur = joueur
                if M[i+3][j] == joueur and M[i+2][j+1] == joueur and M[i+1][j+2] == joueur and M[i][j+3] == joueur:
                    vainqueur = joueur

    return vainqueur

########################################################################################
# Différents niveaux de jeu

def niveau0():
    '''retourne une colonne aléatoire'''
    return verif_colonne(rd.randint(0,6))

def niveau1(M):
    '''vérifie si peut gagner quelque part et y joue, sinon essaie de bloquer l'adversaire'''
    col = -1
    for j in range(7):
        if verif_colonne(j) == j: #si on peut jouer sur cette colonne
            M[ligne(j)][j] = 2
            if verification_P4() == 2:
                col = j
            M[ligne(j)-1][j] = 0
    if col == -1:
        for j in range(7):
            if verif_colonne(j) == j: #si on peut jouer sur cette colonne
                M[ligne(j)][j] = 1
                if verification_P4() == 1:
                    col = j
                M[ligne(j)-1][j] = 0
        if col == -1:
            return niveau0()
        else:
            return col
    else:
        return col

#Méthode minmax avec heuristiques
def heuristique(M):
    '''exemple d'heuristique : calcule le nombre d'endoit où le joueur peut gagner moins le nombre d'endroits où l'adversaire peut gagner '''
    heur = 0
    #teste toutes les possibilités en lignes
    for i in range(6):
        for j in range(4):
            if M[i][j] != 1 and M[i][j+1] != 1 and M[i][j+2] != 1 and M[i][j+3] != 1:
                heur +=1
            if M[i][j] != 2 and M[i][j+1] != 2 and M[i][j+2] != 2 and M[i][j+3] != 2:
                heur -=1


    #teste toutes les possibilités en colonnes
    for j in range(7):
        for i in range(3):
            if M[i][j] != 1 and M[i+1][j] != 1 and M[i+2][j] != 1 and M[i+3][j] != 1:
                heur +=1
            if M[i][j] != 2 and M[i+1][j] != 2 and M[i+2][j] != 2 and M[i+3][j] != 2:
                heur -=1

    #teste toutes les possibilités en diagonales montantes / et descendantes \
    for i in range(3):
        for j in range(4):
            if M[i][j] != 1 and M[i+1][j+1] != 1 and M[i+2][j+2] != 1 and M[i+3][j+3] != 1:
                heur +=1
            if M[i+3][j] != 1 and M[i+2][j+1] != 1 and M[i+1][j+2] != 1 and M[i][j+3] != 1:
                heur +=1
            if M[i][j] != 2 and M[i+1][j+1] != 2 and M[i+2][j+2] != 2 and M[i+3][j+3] != 2:
                heur -=1
            if M[i+3][j] != 2 and M[i+2][j+1] != 2 and M[i+1][j+2] != 2 and M[i][j+3] != 2:
                heur -=1

    return heur

def heuristique2(M):
        '''Heuristique un peu plus complexe'''
        somme = 0
        # colonnes
        for j in range(7):  #colonnes
            for i in range(3):  #lignes
                zone =[M[i][j], M[i+1][j], M[i+2][j], M[i+3][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += (1000)
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count(1)
        # lignes
        for i in range(6):     #lignes
            for j in range(4):  #colonnes
                zone = [M[i][j], M[i][j+1], M[i][j+2], M[i][j+3]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += (1000)
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count(1)
        # diagonales haut-droites
        for i in range(3):
            for j in range(4):
                zone = [M[i][j+3], M[i+1][j+2], M[i+2][j+1], M[i+3][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += (1000)
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count(1)
        # diagonales haut-gauches
        for i in range(3):
            for j in range(4):
                zone = [M[i+3][j+3], M[i+2][j+2], M[i+1][j+1], M[i][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += (1000)
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count(1)

        return somme

def list_minmax(M,profondeur,profondeur_initiale,liste):
    '''calcule la liste des heuristiques pour une profondeur donnée''' 
    if profondeur == 1:
        for col in range(7):
            if colonne_disponible(M,col):
                M[ligne(col)][col] = (profondeur_initiale - profondeur + 1)%2 +1
                liste.append(heuristique2(M))
                M[ligne(col)-1][col] = 0 
            else:
                liste.append(np.nan)
    else:
        liste_ce_niveau = list(liste)
        for col in range(7):
            if colonne_disponible(M,col):
                M[ligne(col)][col] = (profondeur_initiale - profondeur + 1)%2 +1
                liste.append(list_minmax(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
                M[ligne(col)-1][col] = 0
            else:
                liste.append(list_nan(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))

    return liste

def list_nan(M,profondeur,profondeur_initiale,liste):
    '''retrourne la liste de nan'''
    if profondeur == 1:
        for col in range(7):
            liste.append(np.nan)
    else:
        liste_ce_niveau = list(liste)
        for col in range(7):
            liste.append(list_nan(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
    return liste



def minmax(liste):
    '''applique l'algorithme minmax à la liste des états possibles du jeu futur'''
    if type(liste[0]) != list:
        return liste.index(vrai_max(liste)) 
    else:
        for i in range(len(liste)):
            liste[i] = min_spec(liste[i])
        print(liste,liste.index(vrai_max(liste)))
        return liste.index(vrai_max(liste))

def max_spec(liste):
    print(liste)
    '''partie max recursive de l'algorithme'''
    if type(liste[0]) != list:
        return vrai_max(liste)
    else:
        for i in range(len(liste)):
            liste[i] = min_spec(liste[i])
        return max_spec(liste)


def min_spec(liste):
    print(liste)
    '''partie min recursive de l'algorithme'''
    if type(liste[0]) != list:
        return vrai_min(liste)
    else:
        for i in range(len(liste)):
            liste[i] = max_spec(liste[i])
        return min_spec(liste)

def vrai_max(liste):
    '''retourne le maximum d'une liste avec des nan'''
    if liste == 7 * [np.nan]:
        return np.nan
    n = len(liste)
    maximum = -inf
    for i in range(n):
        element = liste[i]
        if type(element) == int and element>maximum:
            maximum = element
    return maximum

def vrai_min(liste):
    '''retourne le minimum d'une liste avec des nan'''
    if liste == 7 * [np.nan]:
        return np.nan 
    n = len(liste)
    minimum = inf
    for i in range(n):
        element = liste[i]
        if type(element) == int and element<minimum:
            minimum = element
    return minimum


def get_column(niveau):
    '''retourne la colonne où joue l'IA en fonction du niveau souhaité'''
    if int(niveau) == 0 :
        return niveau0() 
    elif int(niveau) == 1:
        return niveau1(M)
    elif int(niveau) > 1:
        return minmax(list_minmax(M,min(int(niveau)-1,4),min(int(niveau)-1,4),[]))

################################################################################
#Let's play !
niveau = input("Entrez le niveau de difficulté souhaité entre 0 et 5, 5 étant le plus compliqué :")
while (P4 == 0 and JetonsJoues < 42):
    # Le joueur joue
    for event in pygame.event.get():
        #Le joueur joue
        if event.type == pygame.MOUSEBUTTONUP :
            x,y = pygame.mouse.get_pos()
            joueur = quel_joueur()
            colonne = choisir_colonne(x,y)
            # On modifie les variables pour tenir compte du jeton depose.
            M[ligne(colonne)][colonne] = joueur
            JetonsJoues = JetonsJoues + 1
            affichage(M)
            pygame.display.flip()
            #L'IA répond
            joueur = quel_joueur()
            colonne = get_column(niveau)
            M[ligne(colonne)][colonne] = joueur
            JetonsJoues = JetonsJoues + 1
            P4 = verification_P4()
            affichage(M)
            pygame.display.flip()
            time.sleep (0.5)
        if event.type == pygame.QUIT:
            sys.exit()


if P4 != 0:
    print('Joueur',P4,'a gagné !')
elif JetonsJoues == 42:
    print('Plus de jeton disponible, égalité')
else:
    print('Jeu interrompu')

