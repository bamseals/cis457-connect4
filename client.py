import socket

default_ip = "127.0.0.1"
default_port = 4444

class Client:
    def __init__(self, ip, port):
        self.socket = None
        self.ip = ip
        self.port = port
        self.connected = False
        self.buffer = 1024

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.ip, int(self.port)))
        except:
            print("Could not connect to the server")
            self.socket.close()
            return False
        print(f"Connected on {self.ip}:{self.port}")
        self.connected = True
        self.gameLoop()

    def gameLoop(self):
        message = self.socket.recv(self.buffer).decode('utf-8')
        print(message)

        # Game Logic will go here

        self.disconnect()

    def disconnect(self):
        self.socket.close()
        print("Game Ended")

            
            

client = Client(default_ip, default_port)
client.run()
