import math
from game import Game

class TextView:
    def __init__(self, game: Game):
        self.game = game

    def show(self):
        def padStr(s: str, desiredLength: int, padChar: str = " "):
            '''pads string (keeping it centered)
            '''
            switch = False
            while len(s) < desiredLength:
                if switch:
                    s = padChar + s
                else:
                    s = s + padChar
                switch = not switch
            return s

        def numLength(n):
            if n == 0:
                return 1
            else:
                return int(1 + math.log10(n))
        board = self.game.board
        boardWidth = self.game.width
        # boardHeight = len(board)
        maxCellWidth = max(map(lambda row: max(map(numLength, row)), board))
        # ┐└ ┘ ┌ ┴ ┬ ├ ─ ┼ │ ┤
        dashes = "─"*maxCellWidth

        def makeLine(start, mid, end, content):
            return start + mid.join(content) + end
        topLine = makeLine("┌", "┬", "┐", [dashes for _ in range(boardWidth)])
        midLine = makeLine("├", "┼", "┤", [dashes for _ in range(boardWidth)])
        bottomLine = makeLine(
            "└", "┴", "┘", [dashes for _ in range(boardWidth)])

        def boardLine(row):
            rowStrs = map(lambda n: padStr(
                ("" if n == 0 else str(n)), maxCellWidth), row)
            return makeLine("│", "│", "│", rowStrs)
        boardLines = map(boardLine, board)

        def intercalate(sep, l):
            ans = []
            for x in l:
                ans.append(x)
                ans.append(sep)
            return ans[:-1]
        lines = [topLine] + intercalate(midLine, boardLines) + [bottomLine]
        ans = "\n".join(lines)
        if self.game.isDead():
            ans += f"\nGame Over. Score: {self.game.score()}"
        return ans
