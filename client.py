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
        message = self.receiveMsg()
        lines = message.split("\0")
        for line in lines:
            if (line == 'end'):
                self.disconnect()
            elif "Your turn, pick a column" in line:
                msg = input("Your turn, pick a column: ")
                self.sendMsg(msg)
            else:
                print(line)
        self.gameLoop()

    def receiveMsg(self):
        message = self.socket.recv(self.buffer).decode('utf-8')
        return message

    def sendMsg(self, msg):
        encode = (msg+'\0').encode('utf-8')
        self.socket.send(encode)

    def disconnect(self):
        self.socket.close()
        print("Game Ended")

            
            

client = Client(default_ip, default_port)
client.run()
