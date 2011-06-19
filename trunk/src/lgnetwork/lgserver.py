from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from lgnetwork.lgnetworkcommon import LgNetworkCommon

class LgServer(object):
    def __init__(self, model):
        self.playerDict = {}
        self.model = model
        
    class ClientThread(Thread, LgNetworkCommon):
        def __init__(self, channel, details):
            self.channel = channel
            self.details = details
            LgNetworkCommon.__init__(self)
            Thread.__init__(self)       
            self.isGameStarted = False
            
        def run(self):
            if not self.isGameStarted:
                return
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
            self.playerDict[playerID] = self.ClientThread(channel, details)
            self.playerDict[playerID].start()
            playerID += 1
            if len(self.playerDict) == len(self.model.players):
                playersSet = True
        for player in self.playerDict.values():
            player.isGameStarted = True
            
    def processNetworkCommuncation(self, currentPlayerIndex):
        self.playerDict[currentPlayerIndex].setData(self.model.getData())
        self.playerDict[currentPlayerIndex].run()
        self.playerDict[currentPlayerIndex].join()
        self.model.setData(self.playerDict[currentPlayerIndex].getData())
        
    def endNetworkCommunication(self):
        for id in xrange(len(self.playerDict)):
            self.playerDict[id].setIsFinish(True)
            self.playerDict[id].start()
    
    def isServer(self):
        return True