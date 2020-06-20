import numpy as np
from vector import Vector
import random

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
directions = [UP, DOWN, LEFT, RIGHT]

class Game:
    def __init__(self, board=None, allPositions=None):
        self.width = 4
        self.height = 4
        self.board = board
        if board is None:
            self.board = np.array([[0 for _ in range(self.width)] for _ in range(self.height)])
        self.allPositions = allPositions
        if allPositions is None:
            self.allPositions = [Vector(x, y) for x in range(self.width) for y in range(self.height)]
        if board is None:
            self.spawnTile()
            self.spawnTile()
    
    def copy(self):
        game = Game(np.copy(self.board), self.allPositions)
        return game
    
    def valAtVec(self, p):
        return self.board[p.y][p.x]
    
    def setVec(self, p, n : int):
        self.board[p.y][p.x] = n
    
    def getFreePos(self):
        '''returns a position which is not occupied by a non-zero number
        '''
        def isGoodPosition(p):
            return self.valAtVec(p) == 0
        goodPositions = list(filter(isGoodPosition, self.allPositions))
        try:
            return random.choice(goodPositions)
        except IndexError:
            # no free positions
            return None
    
    def getCondensedCol(self, c):
        col = self.board[:, c]
        return self.condense(col)
    
    def getCondensedRow(self, r):
        row = self.board[r]
        return self.condense(row)
    
    def setRow(self, r, row):
        self.board[r] = row
    
    def setCol(self, c, col):
        self.board[:, c] = col
    
    def condense(self, nums):
        nums = list(filter(lambda x: x > 0, nums))
        # def help(l : list):
        #     '''functional programming ftw!
        #     '''
        #     if len(l) <= 1:
        #         return l
        #     else:
        #         first = l[0]
        #         second = l[1]
        #         rest = l[2:]
        #         if first == second:
        #             return [2*first] + help(rest)
        #         else:
        #             return [first] + help([second] + rest)
        # nums = help(nums)
        # return nums
        i = 0
        while i < len(nums)-1:
            cur = nums[i]
            next_ = nums[i+1]
            if cur == next_:
                del nums[i+1]
                nums[i] *= 2
            i += 1
        return nums

    def spawnTile(self):
        p = self.getFreePos()
        n = 2
        if random.randint(1, 10) == 1:
            n = 4
        self.setVec(p, n)
    
    def move(self, direction):
        '''direction is either UP, DOWN, LEFT, or RIGHT
        '''
        old = self.copy()
        def pad(items, padItem, desiredLength, fromFront=True):
            lenitems = len(items)
            if lenitems < desiredLength:
                pads = [padItem for _ in range(desiredLength - lenitems)]
                if fromFront:
                    items = pads + items
                else:
                    items += pads
            return items

        away = direction in [DOWN, RIGHT]
        if direction in [DOWN, UP]:
            condensedCols = [self.getCondensedCol(c) for c in range(self.width)]
            condensedCols = [pad(col, 0, self.height, fromFront=away) for col in condensedCols]
            for c, col in enumerate(condensedCols):
                self.setCol(c, col)
        else:
            condensedRows = [self.getCondensedRow(r) for r in range(self.height)]
            condensedRows = [pad(row, 0, self.width, fromFront=away) for row in condensedRows]
            for r, row in enumerate(condensedRows):
                self.setRow(r, row)

        if old != self:
            # the move actually did something
            self.spawnTile()
        
    def isDead(self):
        for direction in directions:
            g = self.copy()
            g.move(direction)
            if g != self:
                return False
        return True
    
    def score(self):
        '''like performance points in osu
        rewards few, high squares. so an 8 is worth more than 2 4's
        '''
        flat = list(filter(lambda x: x > 0, self.board.flatten()))
        asc = sorted(flat)
        score = 0
        for val in asc:
            score += val
            score *= .9

        # score /= len(asc) # minimize live tiles

        return score

    def __eq__(self, other):
        try:
            return (self.board == other.board).all()
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.board)

