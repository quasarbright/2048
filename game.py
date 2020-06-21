import numpy as np
from vector import Vector
from random import Random
random = Random()

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
directions = [UP, DOWN, LEFT, RIGHT]

# a snaking hamiltonian path of the grid
'''
>────┐
┌────┘
└────┐
<────┘
'''
snakeVectors = [
    Vector(0,0),Vector(1,0),Vector(2,0),Vector(3,0),
    Vector(3,1),Vector(2,1),Vector(1,1),Vector(0,1),
    Vector(0,2),Vector(1,2),Vector(2,2),Vector(3,2),
    Vector(3,3),Vector(2,3),Vector(1,3),Vector(0,3),
]

snakePaths = [
    snakeVectors
]
snakePaths += [snakeVectors[::-1] for snakeVectors in snakePaths] # reverse
snakePaths += [[Vector(p.y, p.x) for p in snakeVectors] for snakeVectors in snakePaths] # transpose
snakePaths += [[Vector(3 - p.x, p.y) for p in snakeVectors] for snakeVectors in snakePaths] # vert refl
snakePaths += [[Vector(p.x, 3 - p.y) for p in snakeVectors] for snakeVectors in snakePaths] # horiz refl
snakePaths = list(set(map(tuple, snakePaths)))# remove duplicates
# all unique snaky paths
# 1 path per square symmetry in the D4 group


class Game:
    def __init__(self, board=None, allPositions=None):
        self.width = 4
        self.height = 4
        self.seed = random.random()
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
        game.seed = self.seed
        return game
    
    def valAtVec(self, p):
        return self.board[p.y, p.x]
    
    def setVec(self, p, n : int):
        self.board[p.y, p.x] = n
    
    def isFreePos(self, p):
        return self.valAtVec(p) == 0
    
    def getFreePos(self):
        '''returns a position which is not occupied by a non-zero number
        '''
        random.seed(self.seed)
        
        goodPositions = list(filter(self.isFreePos, self.allPositions))
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
        # actually random
        random.seed(self.seed)
        p = self.getFreePos()
        n = 2
        if random.randint(1, 10) == 1:
            n = 4
        # best possible luck
        # for p in snakeVectors:
        #     if self.isFreePos(p):
        #         break
        # n = 4
        self.setVec(p, n)



    
    def move(self, direction):
        '''direction is either UP, DOWN, LEFT, or RIGHT
        '''
        assert direction in directions
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
            self.board = np.transpose(np.array(condensedCols))
        else:
            condensedRows = [self.getCondensedRow(r) for r in range(self.height)]
            condensedRows = [pad(row, 0, self.width, fromFront=away) for row in condensedRows]
            self.board = np.array(condensedRows)

        if old != self:
            # the move actually did something
            self.seed += 1
            self.spawnTile()
        
    def isDead(self):
        if np.min(self.board) == 0:
            return False
        for direction in directions:
            g = self.copy()
            g.move(direction)
            if g != self:
                return False
        return True
    
    def score(self):
        '''encourages tiles to be arranged in a snaking pattern and in decreasing order
        '''
        def pathScore(snakeVectors):
            snaked = list(map(self.valAtVec, snakeVectors))
            score = 0
            for val in snaked:
                score *= .5
                score += val
            if self.isDead():
                score /= 10
            return score
        return max(map(pathScore, snakePaths))
    
    def userScore(self):
        return np.sum(self.board)

    def __eq__(self, other):
        try:
            return (self.board == other.board).all()
        except AttributeError:
            return False

    def __hash__(self):
        return hash(tuple(self.board.flatten()))

