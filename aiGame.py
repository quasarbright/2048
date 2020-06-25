from game import Game, UP, DOWN, LEFT, RIGHT, directions

class AIGame:
    def __init__(self, game):
        self.game = game
    
    def getAllMoves(self):
        return directions[:]

    def getLegalMoves(self):
        return list(filter(self.isMoveLegal, self.getAllMoves()))

    def isMoveLegal(self, move):
        g = self.game.copy()
        g.move(move)
        return g != self.game
    
    def isTerminalState(self):
        return self.game.isDead()
    
    def score(self):
        return self.game.score()
    
    def move(self, move):
        newGame = self.game.copy()
        newGame.move(move)
        return AIGame(newGame)
    
    def __eq__(self, other):
        try:
            return self.game == other.game
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash(self.game)