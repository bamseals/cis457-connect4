class Board:
    def __init__(self):
        self.turn = 0 # how many turns have been taken in the game
        self.playerturn = 1 # which player's turn it is, 1 or 2
        self.rows = 6
        self.cols = 7
        self.board = self.buildBoard()

    def buildBoard(self):
        board = {}
        for r in range(self.rows):
            board[r] = {}
            for c in range(self.cols):
                board[r][c] = ''
        return board
