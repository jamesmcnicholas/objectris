import socket
import pickle


class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.61"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.board = self.connect()

    def getBoard(self):
        return self.board

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)