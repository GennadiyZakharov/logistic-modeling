from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from lgnetwork.lgnetworkcommon import NetworkCommon

class LgServer(object):
    def __init__(self, model):
        self.playerDict = {}
        self.model = model
        
    class ClientThread(Thread, NetworkCommon):
        def __init__(self, channel, details):
            self.channel = channel
            self.details = details
            Thread.__init__(self)       
            
        def run(self):
            if not self.isFinish:
                self.send()
                self.receive()
            else:
                self.channel.close()
                        
    def createGame(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 9000))
        s.listen(5)  
        playersSet = False  
        while not playersSet:
            channel, details = s.accept()
            # TODO: Set player ID to client thread 
            playerID = None
            self.playerDict[playerID] = self.ClientThread(channel, details, playerID)
            if len(self.playerDict) == self.model.playersCount:
                playersSet = True
    
    def runGame(self):
        while not self.model.isFinished():
            for id in xrange(len(self.playerDict)):
                self.playerDict[id].setData(self.model.getData())
                self.playerDict[id].start()
                self.model.setData(self.playerDict[id].getData())
        # Disconnect clients
        for id in xrange(len(self.playerDict)):
            self.playerDict[id].setIsFinish(True)
            self.playerDict[id].start()
