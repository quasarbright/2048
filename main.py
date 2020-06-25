import sys
import random
import time
from game import Game, UP, DOWN, LEFT, RIGHT, directions
from textView import TextView
from aiGame import AIGame
import minimax
import montecarlo
game = Game()
view = TextView(game)
def show():
    print(view.show())

def move(direction):
    game.move(direction)
    show()


show()

depth = 5

def chooseAction(game):
    return minimax.chooseAction(game, depth)
    # actions = game.getAllMoves()
    # return random.choice(actions)
    # return montecarlo.chooseAction(game, depth)

if len(sys.argv) > 1:
    depth = int(sys.argv[1])
while not game.isDead():
    move(chooseAction(AIGame(game)))
    # print(game.score())
    # print()
print("search depth used:",depth)