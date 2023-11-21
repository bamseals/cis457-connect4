class Board:
    def __init__(self):
        self.turn = 0  # how many turns have been taken in the game
        self.player_turn = 1  # which player's turn it is, 1 or 2: red/blue (gui) or X/O (ascii)
        self.rows = 6
        self.cols = 7
        self.board = self.buildBoard()
        self.last_move = [0, 0]

    def buildBoard(self):
        """
        Builds an internal board representation, filling it with 0's

        :return: A zeroed out board, made of two dictionaries
        """
        board = {}
        for r in range(self.rows):
            board[r] = {}
            for c in range(self.cols):
                board[r][c] = 0
        return board

    ## TODO Win conditions are NOT finished. WIP
    def check_win(self, move):
        """

        :param move: A coordinate array, [x, y] of the location of the piece that was dropped
        :return: Whether the move caused the player to win
        """

        y = move[0]
        x = move[1]
        win = False

        # Horizontal Check
        curr_4 = []
        for i in range(max(0, x - 3), min(self.cols - 1, x + 4)):
            count = 0
            curr_4.append(self.board[i][y])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True

        # Vertical Check
        x = move[1]
        curr_4 = []
        for i in range(max(0, y - 3), min(self.rows, y + 4)):
            count = 0

            curr_4.append(self.board[x][i])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True

        # Bottom left to top right diagonal
        y = move[0]
        x = move[1]
        y += 3
        if y > 5:
            y = 5
        curr_4 = []
        for i in range(max(0, x - 3), min(self.cols - 1, x + 4, y)):
            count = 0
            curr_4.append(self.board[i][y])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True
            y -= 1

        # Top Left to bottom right diagonal
        r = move[0]
        c = move[1]
        c -= 3
        if c < 0:
            c = 0
        curr_4 = []
        for i in range(max(0, r - 3), min(self.rows, r + 4)):
            count = 0
            curr_4.append(self.board[i][y])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True
            c += 1
        return win

    def check_tie(self):
        """
        Checks for a tie by looking for available spaces on the board, and whether a move finished the game.
        If there are no available spaces, there is a tie.

        :return: Whether the game is at a tie
        """
        if self.check_win(self.last_move):
            return False

        tie = True
        for row in self.board:
            for col in self.board[row]:
                if col == 0:
                    tie = False
        return tie

    def place_piece(self, column):
        """
        Places a piece into the first available space in the column

        :param column: Which column to drop the piece into
        :return: null
        """
        col = []
        for r in range(self.rows):
            col.append(self.board[r][column])
        i = 0

        # Locate the highest row that has been placed in
        while col[i] == 0:
            i += 1
            if i == self.rows:
                break

        print("Placing! ", self.player_turn)
        self.board[i - 1][column] = self.player_turn
        self.last_move = [i - 1, column]
        return

    def print_board(self):
        """
        Prints the board after converting it to Strings
        Due to the way 2D arrays are printed, it is necessary to print within the function

        :return: null
        """
        pboard = {}
        for r in range(self.rows):
            pboard[r] = {}
            for c in range(self.cols):
                curr = self.board[r][c]
                if curr == 0:
                    pboard[r][c] = '[]'
                elif curr == 1:
                    pboard[r][c] = 'X'
                elif curr == 2:
                    pboard[r][c] = 'O'

        barr = []
        for r in range(self.rows):
            rarr = []
            for c in range(self.cols):
                rarr.append(pboard[r][c])
            barr.append(rarr)

        for r in range(self.rows):
            print(barr[r])
        return

    def next_turn(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1


# Some small testing
b = Board()
b.buildBoard()
# x
b.place_piece(3)
b.next_turn()
# o
b.place_piece(4)
b.next_turn()
# x
b.place_piece(4)
b.next_turn()
# o
b.place_piece(5)
b.place_piece(5)
b.next_turn()
# x
b.place_piece(5)
b.next_turn()
# o
b.place_piece(6)
b.place_piece(6)
b.place_piece(6)
b.next_turn()
# x
b.place_piece(6)
print(b.board)
# print(b.check_win(b.last_move))
print(b.print_board())
