#!/usr/bin/python3.5
import kivy
kivy.require('1.0.6') # ici votre version de kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle,Line, Ellipse
from player import HumanPlayer
from aiplayer import AIPlayerRandom, AIPlayerDebutantAA, AIPlayerIntermediaireAA
import time

class Grille(GridLayout):

    def __init__(self, **kwargs):
        super(Grille, self).__init__(**kwargs)
        self.cols = 7
        self.rows = 6
        self.spacing = 2

        self.quickaccess = []

        for i in range(42):
            circ = Puiss4Circle(i)
            self.quickaccess.append(circ)
            self.add_widget(circ)

class Puiss4Circle(RelativeLayout):
    def __init__(self, i, **kwargs):
        super(Puiss4Circle, self).__init__(**kwargs)
        self.update(0)

    def update(self, color):
        with self.canvas.before:
            if color>0:
                Color(0,0,1,1)
            elif color<0:
                Color(1,0,0,1)
            else:
                Color(1,1,1,1)
            Ellipse(pos=self.to_widget(self.pos[0]+10,self.pos[1]+10), size=[40,40])



class ControlBar(GridLayout):

    def __init__(self, **kwargs):
        super(ControlBar, self).__init__(**kwargs)
        self.cols = 7
        self.quickaccess = []
        for i in range(7):
            b = Button(text='V', size_hint_x=None, width=60)
            self.add_widget(b)
            self.quickaccess.append(b)

    def changeColorButton(self, color):
        for button in self.quickaccess:
            with button.canvas.before:
                if color>0:
                    button.background_color = [0,0,1,1]
                else:
                    button.background_color = [1,0,0,1]

    def disableButton(self, index):
        self.quickaccess[index].disabled = True
        self.quickaccess[index].text = ""

    def activateButtons(self):
        for button in self.quickaccess:
            if button.text != "":
                button.disabled = False

    def deactivateButtons(self):
        for button in self.quickaccess:
            button.disabled = True



class Puiss4MainControl(GridLayout):

    def __init__(self, player1, player2, **kwargs):
        super(Puiss4MainControl, self).__init__(**kwargs)
        self.rows = 2
        self.padding = [20,20]
        self.spacing = [0, 30]

        self.__controlbar = ControlBar(size_hint_y=None, height=50)
        for butt in self.__controlbar.quickaccess:
            butt.bind(on_press=self.buttonPressed)
        self.add_widget(self.__controlbar)
        self.grille = Grille()
        self.add_widget(self.grille)

        #model
        self.model = [[0 for i in range(6) ] for j in range(7)]

        #joueurs
        player1.color = -1
        player2.color = 1
        self.players = [player1, player2]

        #partie
        self.__currentplayer = 0
        self.__updateCurrentPlayer()
        self.__waitForPlayer()


    def __waitForPlayer(self):
        if (isinstance(self.players[self.__currentplayer],AIPlayerRandom) or isinstance(self.players[self.__currentplayer],AIPlayerDebutantAA) or isinstance(self.players[self.__currentplayer],AIPlayerIntermediaireAA)):
            #on interroge l'IA
            #print(self.players[self.__currentplayer].heuristic(self.model))
            index = self.players[self.__currentplayer].getColumn(self.model)
            if 0<=index<7 and self.model[index][-1]==0:
                #le coup est bon on joue
                self.__updateModel(index)

            #Fin de partie
            res = self.__isGameFinished()
            if res[0]:
                self.__onGameFinished(res[1], res[2])

            #on passe au joueur suivant
            self.__currentplayer = (self.__currentplayer + 1)%2
            self.__updateCurrentPlayer()
            self.__waitForPlayer()
        else:
            #c'est un joueur humain, rien à faire
            pass


    def buttonPressed(self,instance):
        selectedbutton = self.__controlbar.quickaccess.index(instance)

        self.__updateModel(selectedbutton)

        #Fin de partie
        res = self.__isGameFinished()
        if res[0]:
            self.__onGameFinished(res[1], res[2])


        #on passe au joueur suivant
        self.__currentplayer = (self.__currentplayer + 1)%2
        self.__updateCurrentPlayer()
        self.__waitForPlayer()


    def __isGameFinished(self):
        grille = self.model

        #lignes
        for i in range(6):
            for j in range(4):
                somme = grille[j][i] + grille[j+1][i] + grille[j+2][i] + grille[j+3][i]
                if somme == 4:
                    return True, 1, "ligne"
                elif somme == -4:
                    return True, -1, "ligne"

        #colonnes
        for j in range(7):
            for i in range(3):
                somme = grille[j][i] + grille[j][i+1] + grille[j][i+2] + grille[j][i+3]
                if somme == 4:
                    return True, 1, "colonne"
                elif somme == -4:
                    return True, -1, "colonne"

        #diagonales
        for i in range(3):
            for j in range(3):
                somme = grille[j][i] + grille[j+1][i+1] + grille[j+2][i+2] + grille[j+3][i+3]
                if somme == 4:
                    return True, 1, "diagonale"
                elif somme == -4:
                    return True, -1, "diagonale"
        for i in range(3):
            for j in range(3,7):
                somme = grille[j][i] + grille[j-1][i+1] + grille[j-2][i+2] + grille[j-3][i+3]
                if somme == 4:
                    return True, 1, "diagonale"
                elif somme == -4:
                    return True, -1, "diagonale"

        #match nul
        for i in range(7):
            if grille[i][-1]==0:
                return (False, None, None)

        return (True, 0, None)


    def __onGameFinished(self, winner, reason):
        if winner<0:
            print("Le joueur rouge a gagne grace a une %s"%reason)
        elif winner==0:
            print("match nul")
        else:
            print("Le joueur bleu a gagne grace a une %s"%reason)
        App.get_running_app().stop()


    def __updateCurrentPlayer(self):
        self.__controlbar.changeColorButton(self.players[self.__currentplayer].color)

        if (isinstance(self.players[self.__currentplayer],AIPlayerRandom) or isinstance(self.players[self.__currentplayer],AIPlayerDebutantAA) or isinstance(self.players[self.__currentplayer],AIPlayerIntermediaireAA)):            #on masque les boutons
            self.__controlbar.deactivateButtons()
        else:
            #on affiche les boutons
            self.__controlbar.activateButtons()


    def __updateModel(self,col):
        row = 0
        while row < len(self.model[col]) and self.model[col][row]!=0: row+=1
        self.model[col][row] = self.players[self.__currentplayer].color
        #mise à jour de la couleur de la case
        self.grille.quickaccess[(5-row)*7+col].update(self.players[self.__currentplayer].color)
        #desactivation du compteur si necessaire
        if row == 5:
            self.__controlbar.disableButton(col)



class Puiss4(App):

    def build(self):
        return Puiss4MainControl(HumanPlayer(), AIPlayerIntermediaireAA())


if __name__ == '__main__':
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'height', '460')
    Config.set('graphics', 'width', '460')

    while True:
        Puiss4().run()
        print("voulez-vous faire une autre partie (o/n)?")
        res = input()
        if res!='O' and res!='o':
            break
