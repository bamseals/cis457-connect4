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
        turn = -1
        while turn < 0 or turn > b.cols-1:
            turn = input(input_string)
            if turn == 'quit' or turn == 'q':
                return "Quitting! Thanks for Playing!"
            turn = int(turn)
        result = b.place_piece(turn)
        if result == "Illegal place":
            print("Illegal place")
        else:
            win, tie = result
        b.print_board()
    return curr_player + " Won!"


print(main())
