import random
memo = {}
def chooseAction(game, maxDepth=10):
    def value(game, depth):
        actions = game.getAllMoves()
        if (game, depth) in memo:
            return memo[(game, depth)]
        if depth == 0 or len(actions) == 0:# or game.isTerminalState():
            ans = game.score()
            memo[(game, depth)] = ans
            return ans
        else:
            newGames = [game.move(actions) for action in actions]
            ans = max([value(game, depth-1) for game in newGames])
            memo[(game, depth)] = ans
            return ans
    def valueOfAction(action):
        newGame = game.move(action)
        return value(newGame, maxDepth)
    actions = game.getLegalMoves()
    random.shuffle(actions)
    return max(actions, key=valueOfAction)
