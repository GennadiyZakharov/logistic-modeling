from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from lgnetwork.lgnetworkcommon import NetworkThreadCommon

class LgServer(object):
    def __init__(self, model):
        self.playerDict = {}
        self.model = model
        
    class ClientThread(Thread, NetworkThreadCommon):
        def __init__(self, channel, details):
            self.channel = channel
            self.details = details
            NetworkThreadCommon.__init__(self)
            Thread.__init__(self)       
            
        def run(self):
            if not self.isFinish:
                self.send()
                self.receive()
            else:
                self.channel.close()
                        
    def createGame(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 1234))
        s.listen(5)  
        playersSet = False  
        playerID = 0
        print 'Awaiting connections...'
        while not playersSet:
            channel, details = s.accept()
            print 'Accepted connection from {0}'.format(str(details))           
            self.playerDict[self.model.players[playerID]] = self.ClientThread(channel, details)
            playerID += 1
            if len(self.playerDict) == len(self.model.players):
                playersSet = True
    
    def processNetworkCommuncation(self, currentPlayerIndex):
        currentPlayer = self.model.players[currentPlayerIndex]
        self.playerDict[currentPlayer].setData(self.model.getData())
        self.playerDict[currentPlayer].start()
        self.playerDict[currentPlayer].join()
        self.model.setData(self.playerDict[currentPlayer].getData())
        
    def endNetworkCommunication(self):
        for id in xrange(len(self.playerDict)):
            self.playerDict[id].setIsFinish(True)
            self.playerDict[id].start()
    
    def isServer(self):
        return True