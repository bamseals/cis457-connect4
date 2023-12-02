import board as bd

def main():
    # Some small testing
    b = bd.Board()
    b.buildBoard()

    print("Welcome to Connect 4. This version is for two people to play on the same device against each other.")
    # print("Player 1 (X) goes first! Please choose a column 0-6 to place into.")

    win = False
    tie = False
    curr_player = ""
    while not win and not tie:
        if b.player_turn == 1:
            curr_player = "Player 1 (X)"
        if b.player_turn == 2:
            curr_player = "Player 2 (O)"
        input_string = curr_player + ", Please enter a column 0-6: "
        turn = input(input_string)
        turn = int(turn)
        win, tie = b.place_piece(turn)
        b.print_board()
    return curr_player + " Won!"

print(main())
