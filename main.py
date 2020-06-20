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

depth = 5
while not game.isDead():
    move(minimax.chooseAction(AIGame(game), maxDepth=depth))
print("search depth used:",depth)