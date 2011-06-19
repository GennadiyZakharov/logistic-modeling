from socket import socket, AF_INET, SOCK_STREAM
from lgnetwork.lgnetworkcommon import LgNetworkCommon

class LgClient(LgNetworkCommon):
    def __init__(self, serverAddress, serverPort, model):
        self.serverAddress = serverAddress
        self.serverPort = serverPort        
        self.sock = None
        self.model = model
        super(LgClient, self).__init__()
        self.connect()
        
    def connect(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.serverAddress, self.serverPort))        
        print 'Connected to {0}'.format(self.sock.getpeername())
        self.channel = self.sock
        # self.channe
       
    def send(self):
        self.setData(self.model.getData())
        super(LgClient, self).send()
    
    def receive(self):
        super(LgClient, self).receive()
        print self.getData()
        self.model.setData(self.getData())
             
    def isServer(self):
        return False