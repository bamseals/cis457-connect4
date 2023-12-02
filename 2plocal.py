import board as bd

def main():
    # Build the board proper
    b = bd.Board()
    b.buildBoard()

    print("Welcome to Connect 4. This version is for two people to play on the same device against each other.")

    win = False
    tie = False
    curr_player = ""
    while not win and not tie:
        # Store which player's turn it is into a string
        if b.player_turn == 1:
            curr_player = "Player 1 (X)"
        if b.player_turn == 2:
            curr_player = "Player 2 (O)"

        # Formulate the string to be displayed in the prompt
        input_string = curr_player + ", Please enter a column 0-6: "

        # While turn is invalid, keep retrying
        # Turn values that will break out of the loop:
        # - 0, 1, 2, 3, 4, 5, or 6
        # - 'quit' or 'q'
        turn = -1
        while turn < 0 or turn > b.cols-1:
            turn = input(input_string)
            if turn == 'quit' or turn == 'q':
                return "Quitting! Thanks for Playing!"
            turn = int(turn)

        # Place the piece into the column requested
        #   (board automatically calculates whose turn it is)
        result = b.place_piece(turn)

        # If the result was illegal, let the player know
        #   (still their turn)
        if result == "Illegal place":
            print("Illegal place")
        else:
            # Update the while conditions if a turn was done properly.
            win, tie = result
        b.print_board()
    return curr_player + " Won!"


print(main())
