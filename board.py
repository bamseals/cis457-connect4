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
                board[r][c] = '[]'
        return board

    def check_win(self, move, player):
        """
        :param move: A coordinate array, [x, y] of the location of the piece that was dropped
        :param player: Which player made the move, as an int, 0 for red, 1 for blue
        :return: Whether or not the move caused the player to win
        """

        ## TODO: Fill out win checks
        x = move[0]
        y = move[1]
        win = False

        # Horizontal Check
        for i in range(x-3, x+4):
            win = True
        # Vertical Check
        for i in range(y-3, y+4):
            win = True

        #Top left to bottom right diagonal
        y += 3
        for i in range(x-3, x+4):
            win = True
            y -= 1

        # Bottom left to top right diagonal
        x -= 3
        for i in range(y - 3, y + 4):
            win = True
            x += 1

        return win

    def place_piece(self, column):
        return