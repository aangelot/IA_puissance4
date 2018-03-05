import pygame
import sys
import time

#Import images, init game
pygame.init ()
image = pygame.image.load ("Grille.png")
size = image.get_size ()
screen = pygame.display.set_mode (size)
screen.blit (image, (0,0))
pygame.display.flip ()

pionjaune = pygame.image.load ("PionJaune.png")
pionrouge = pygame.image.load ("PionRouge.png")
font = pygame.font.Font ("freesansbold.ttf", 15)

# Variables globales
 
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
# Cette fonction retourne la colonne demandee au joueur1
# Tant que la valeur n'est pas acceptable, on demande la colonne a jouer
    col=x-16
    col=int(col/97)
    while M[5][col] != 0:
    	col = (col+1)%7
    return col


     
def ligne():
# Cette fonction retourne la ligne vide correspondant a la colonne demandee
    lig = 0
    for i in range (1,6):
        if ( M[i][colonne] == 0 and M[i-1][colonne] != 0 ):
            lig = i
    return lig

def verification_P4():
    test2=False
 
    # test d'un P4 horizontal
    i = j = 0
    while(not(i==5 and j==3)):
        if (M[i][j]==M[i][j+1] and M[i][j]==M[i][j+2] \
            and M[i][j]==M[i][j+3] and M[i][j]==joueur):
            test2=True
        if (j==3):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'un P4 vertical
    i = j = 0
    while(not(i==2 and j==6)):
        if (M[i][j]==M[i+1][j] and M[i][j]==M[i+2][j] \
            and M[i][j]==M[i+3][j] and M[i][j]==joueur):
            test2=True
        if (j==6):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'un P4 diagonal vers la droite
    i=j=0
    while(not(i==2 and j==3)):
        if (M[i][j]==M[i+1][j+1] and M[i][j]==M[i+2][j+2] \
            and M[i][j]==M[i+3][j+3] and M[i][j]==joueur):
            test2=True
        if (j==3):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'un P4 diagonal vers la gauche 
    i=0
    j=3
    while(not(i==2 and j==6)):
        if (M[i][j]==M[i+1][j-1] and M[i][j]==M[i+2][j-2] \
            and M[i][j]==M[i+3][j-3] and M[i][j]==joueur):
            test2=True
        if (j==6):
            i=i+1
            j=3
        else:
            j=j+1    
 
    return test2

#Let's play !

while (not P4 and JetonsJoues < 42):
    time.sleep (0.1)
    # Le joueur joue
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP :
            x,y = pygame.mouse.get_pos()
            joueur = quel_joueur()
            colonne = choisir_colonne(x,y)
     # On modifie les variables pour tenir compte du jeton depose.
            M[ligne()][colonne] = joueur
            JetonsJoues = JetonsJoues + 1
            P4 = verification_P4()
            affichage(M)
            pygame.display.flip()
 
 
        if event.type == pygame.QUIT:
            sys.exit()
            

if P4:
	print('Joueur',joueur,'a gagné !')
elif JetonsJoues == 42:
	print('Plus de jetons disponibles, égalité')
else:
	print('Jeu interrompu')


