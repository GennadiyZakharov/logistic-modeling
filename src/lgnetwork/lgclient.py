from socket import socket, AF_INET, SOCK_STREAM
from lgnetwork.lgnetworkcommon import NetworkCommon

class LgClient(NetworkCommon):
    def __init__(self, serverAddress, serverPort):
        self.serverAddress = serverAddress
        self.serverPort = serverPort        
        self.sock = None
        
    def connect(self, serverAddress, serverPort):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.serverAddress, self.serverPort))
        
    def runGame(self):
        while not self.isFinish:
            # TODO: Implement waiting for turn
            self.receive()
            # TODO: Execute turn
            self.send()