from game import Game, UP, DOWN, LEFT, RIGHT, directions

class AIGame:
    def __init__(self, game):
        self.game = game
    
    def getAllMoves(self):
        return directions

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