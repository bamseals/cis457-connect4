import json


class Board:
    def __init__(self):
        self.turn = 0  # how many turns have been taken in the game
        self.player_turn = 1  # which player's turn it is, 1 or 2: red/blue (gui) or X/O (ascii)
        self.rows = 6
        self.cols = 7
        self.board = self.buildBoard()
        self.last_move = [0, 0]
        self.game_over = False

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

    def check_win(self, move):
        """
        Checks locations nearby the move location for winning conditions (4 in a row)

        :param move: A coordinate array, [x, y] of the location of the piece that was dropped
        :return: Whether the move caused the player to win
        """

        # Note: x is rows, y is columns
        x = move[0]
        y = move[1]
        win = False

        # Vertical Check
        curr_4 = []
        for i in range(max(0, x - 3), min(self.rows, x + 4)):
            count = 0
            if win:
                break
            curr_4.append(self.board[i][y])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True

        # Horizontal Check
        curr_4 = []
        for i in range(max(0, y - 3), min(self.cols, y + 4)):
            count = 0
            if win:
                break
            curr_4.append(self.board[x][i])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True

        # Top right to bottom left diagonal
        r = move[0]
        c = move[1]
        c += 3
        r -= 3
        if r < 0:
            c -= 0 - r
            r = 0
        if c > self.cols - 1:
            r += c - (self.cols - 1)
            c = self.cols - 1
        curr_4 = []
        for i in range(r, r + 7):
            count = 0
            if i > self.rows - 1 or c < 0 or win:
                break
            curr_4.append(self.board[i][c])
            if len(curr_4) > 4:
                curr_4.pop(0)
            for j in curr_4:
                if j == self.player_turn:
                    count += 1
            if count == 4:
                win = True
            c -= 1

        # Top Left to bottom right diagonal
        r = move[0]
        c = move[1]
        c -= 3
        r -= 3
        if r < 0:
            c += 0 - r
            r = 0
        if c < 0:
            r += 0 - c
            c = 0
        curr_4 = []
        for i in range(r, r + 7):
            count = 0
            if i > self.rows - 1 or c > self.cols - 1 or win:
                break
            curr_4.append(self.board[i][c])
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
                    break
            if not tie:
                break
        return tie

    def place_piece(self, column):
        """
        Places a piece into the first available space in the column

        :param column: Which column to drop the piece into
        :return: null
        """

        # Generate a column array to iterate through
        col = []
        for r in range(self.rows):
            col.append(self.board[r][column])

        i = 0
        # Locate the highest row that has been placed in
        while col[i] == 0:
            i += 1
            if i == self.rows:
                break
        if i > 0:
            self.board[i - 1][column] = self.player_turn
            self.last_move = [i - 1, column]
            win = self.check_win(self.last_move)
            tie = False
            if not win:
                tie = self.check_tie()
            self.next_turn()
            return win, tie
        else:
            return "Illegal place"  # TODO: adjust this for a redo

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
                    pboard[r][c] = '_'
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

    def serialize_board(self):
        return json.dumps(self.board)

    def next_turn(self):
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1