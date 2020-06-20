import random
import time
from game import Game, UP, DOWN, LEFT, RIGHT, directions
from textView import TextView
from aiGame import AIGame
import minimax
game = Game()
view = TextView(game)
def show():
    print(view.show())

def move(direction):
    game.move(direction)
    show()



show()

while not game.isDead():
    # time.sleep(.5)
    move(minimax.chooseAction(AIGame(game), maxDepth=4))