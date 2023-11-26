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
        self.board = board.Board()
        initial_board = self.board.serialize_board()
        self.sendMsg(self.player1, "Game Starting.....")
        self.sendMsg(self.player2, "Game Starting.....")
        self.sendMsg(self.player1, initial_board)
        self.sendMsg(self.player2, initial_board)
        while self.board.game_over == False:
            if self.board.player_turn == 1:
                self.sendMsg(self.player1, "Your turn, pick a column")
                self.sendMsg(self.player2, "Waiting on Player 1 turn...")
                input = self.receiveMsg(self.player1)
            else:
                self.sendMsg(self.player2, "Your turn, pick a column")
                self.sendMsg(self.player1, "Waiting on Player 2 turn...")
                input = self.receiveMsg(self.player2)
            print(input)
            self.board.next_turn()
               
        # Game Logic goes here
        self.disconnect()

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