##########################
######   MINI-MAX   ######
##########################

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
        """Méthode qui calcule l'heuristique d'un modèle donné"""
        somme = 0
        # colonnes
        for j in range(7):  #colonnes
            for i in range(3):  #lignes
                zone =[M[i][j], M[i+1][j], M[i+2][j], M[i+3][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += float('inf')
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= float('inf')
                    else :
                        somme -= zone.count(1)
        # lignes
        for i in range(6):     #lignes
            for j in range(4):  #colonnes
                zone = [M[i][j], M[i][j+1], M[i][j+2], M[i][j+3]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += float('inf')
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= float('inf')
                    else :
                        somme -= zone.count(1)
        # diagonales haut-droites
        for i in range(3):
            for j in range(4):
                zone = [M[i][j+3], M[i+1][j+2], M[i+2][j+1], M[i+3][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += float('inf')
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= float('inf')
                    else :
                        somme -= zone.count(1)
        # diagonales haut-gauches
        for i in range(3):
            for j in range(4):
                zone = [M[i+3][j+3], M[i+2][j+2], M[i+1][j+1], M[i][j]]
                if not(1 in zone) :
                    if zone.count(2) == 4:
                        somme += float('inf')
                    else :
                        somme += zone.count(2)
                if not (2 in zone) :
                    if zone.count(1) == 4:
                        somme -= float('inf')
                    else :
                        somme -= zone.count(1)

        return somme


class MiniMax:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.currentNode = None     # GameNode
        self.successors = []        # List of GameNodes
        return

    def minimax(self, node):
        # first, find the max value
        best_val = self.max_value(node) # should be root node of tree

        # second, find the node which HAS that max value
        #  --> means we need to propagate the values back up the
        #      tree as part of our minimax algorithm
        successors = self.getSuccessors(node)
        print "MiniMax:  Utility Value of Root Node: = " + str(best_val)
        # find the node with our best move
        best_move = None
        for elem in successors:   # ---> Need to propagate values up tree for this to work
            if elem.value == best_val:
                best_move = elem
                break

        # return that best value that we've found
        return best_move


    def max_value(self, node):
        print "MiniMax-->MAX: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        max_value = -infinity

        successors_states = self.getSuccessors(node)
        for state in successors_states:
            max_value = max(max_value, self.min_value(state))
        return max_value

    def min_value(self, node):
        print "MiniMax-->MIN: Visited Node :: " + node.Name
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        min_value = infinity

        successor_states = self.getSuccessors(node)
        for state in successor_states:
            min_value = min(min_value, self.max_value(state))
        return min_value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value