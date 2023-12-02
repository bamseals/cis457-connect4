import socket
import json

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
            elif "Illegal place" in line:
                print("Illegal place, try again:")
                msg = input("Your turn, pick a column: ")
            elif "Game Over" in line:
                print("Game Over")
                self.disconnect()
            elif line.startswith('{') and line.endswith('}'):
                self.printBoard(line)
            else:
                print(line)
        self.gameLoop()

    def printBoard(self, str):
        array = json.loads(str)
        for row in array:
            rowString = ''
            for col in array[row]:
                if array[row][col] == 0:
                    rowString += '[ ]'
                elif array[row][col] == 1:
                    rowString += '[X]'
                elif array[row][col] == 2:
                    rowString += '[O]'
            print(rowString)

    def receiveMsg(self):
        message = self.socket.recv(self.buffer).decode('utf-8')
        return message

    def sendMsg(self, msg):
        encode = (msg).encode('utf-8')
        self.socket.send(encode)

    def disconnect(self):
        self.socket.close()
        print("Game Ended")

            
            

client = Client(default_ip, default_port)
client.run()
