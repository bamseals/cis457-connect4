import socket
import board

default_ip = "127.0.0.1"
default_port = 4444

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.buffer = 1024
        self.player1 = None # Connection to player 1
        self.player2 = None # Connection to player 2
        self.board = None # Game board
        
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print(f'Server Listening on {self.ip}:{self.port}')

        self.player1, addr1 = self.socket.accept()
        print(f'Player 1 connected from: {addr1}')
        self.sendMsg(self.player1, "You are connected as Player 1, waiting for Player 2...")
        self.player2, addr2 = self.socket.accept()
        print(f'Player 2 connected from: {addr2}')
        self.sendMsg(self.player2, "You are connected as Player 2, starting game...")

        if (self.player1 and self.player2):
            self.gameLoop()
        else:
            print("Error connecting players")
            self.disconnect()

    def gameLoop(self):
        win = False
        tie = False
        self.board = board.Board()
        initial_board = self.board.serialize_board()
        self.sendMsg(self.player1, "Game Starting.....")
        self.sendMsg(self.player2, "Game Starting.....")
        self.sendMsg(self.player1, initial_board)
        self.sendMsg(self.player2, initial_board)
        active = self.player1
        waiting = self.player2
        while not win and not tie:
            if self.board.player_turn == 1:
                active = self.player1
                waiting = self.player2
            else:
                active = self.player2
                waiting = self.player1
            self.sendMsg(active, "Your turn, pick a column")
            self.sendMsg(waiting, f"Waiting on Player {self.board.player_turn} turn...")
            input = self.receiveMsg(active)
            if not input.isnumeric():
                self.sendMsg(active, "Illegal place")
            inputint = int(input)
            result = self.board.place_piece(inputint)
            if result == "Illegal place":
                self.sendMsg(active, result)
            else:
                boardstate = self.board.serialize_board()
                self.sendMsg(waiting, boardstate)
                self.sendMsg(active, boardstate)
                win, tie = result
        # handle how the game ends
        if self.board.player_turn == 1:
            winner = "Player 2"
        else:
            winner = "Player 1"
        if win:
            self.sendMsg(self.player2, winner + " wins the game")
            self.sendMsg(self.player1, winner + " wins the game")
        elif tie:
            self.sendMsg(self.player2, "The game is a tie")
            self.sendMsg(self.player1, "The game is a tie")

        # check if players want to play again
        if self.checkPlayAgain():
            self.gameLoop()
        else:
            self.sendMsg(self.player2, "Game Over")
            self.sendMsg(self.player1, "Game Over")
            self.disconnect()

    def checkPlayAgain(self):
        self.sendMsg(self.player2, "Play again? (y/n)\n")
        self.sendMsg(self.player1, "Play again? (y/n)\n")
        p1input = self.receiveMsg(self.player1)
        p2input = self.receiveMsg(self.player2)
        if ('y' in p1input.lower() and 'y' in p2input.lower()):
            return True
        else:
            return False
        

    def receiveMsg(self, socket):
        message = socket.recv(self.buffer).decode('utf-8')
        return message

    def sendMsg(self, socket, msg):
        encode = (msg+'\0').encode('utf-8')
        socket.send(encode)

    def disconnect(self):
        print("Goodbye")
        self.socket.close()

server = Server(default_ip, default_port)
server.run()