from game import Game, UP, DOWN, LEFT, RIGHT
from textView import TextView
game = Game()
view = TextView(game)
def show():
    print(view.show())

def move(direction):
    game.move(direction)
    show()

def u(): move(UP)
def d(): move(DOWN)
def l(): move(LEFT)
def r(): move(RIGHT)

show()
