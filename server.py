import socket

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
        
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        print(f'Server Listening on {self.ip}:{self.port}')

        self.player1, addr1 = self.socket.accept()
        print(f'Player 1 connected from: {addr1}')
        self.player1.send("You are connected as Player 1, waiting for Player 2...".encode('utf-8'))
        self.player2, addr2 = self.socket.accept()
        print(f'Player 2 connected from: {addr2}')
        self.player2.send("You are connected as Player 2, starting game...".encode('utf-8'))

        if (self.player1 and self.player2):
            self.gameLoop()
        else:
            print("Error connecting players")
            self.disconnect()

    def gameLoop(self):
        # Game Logic goes here
        self.disconnect()

    def disconnect(self):
        print("Goodbye")
        self.socket.close()

server = Server(default_ip, default_port)
server.run()