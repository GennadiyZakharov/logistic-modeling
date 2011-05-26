
from PyQt4 import QtCore
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.lgplayer import LgPlayer
from lgcore.signals import signalTransport, signalNextTurn



class LgModel(QtCore.QObject):
    '''
    This is holder class for all logistic system
    It contains all nodes, links and packages
     Lgmodel is parent for all lg items
    
    It also  contains all payed data
    '''
    def __init__(self):
        super(LgModel, self).__init__()
        self.players = []
        self.teacher = LgPlayer('Teacher',self)
        self.addPlayer(self.teacher)
        self.links = set()
        self.nodes = set()
        self.packages = set()
    
    def addPlayer(self, player):
        player.setParent(self)
        self.players.append(player)
    
    def delPlayer(self, player):
        player.setParent(None)
        for node in self.nodes :
            node.viewers.discard(player)
            if node.owner is player :
                node.setOwner(None)
        self.players.remove(player)
    
    def addNode(self, node):
        node.setParent(self)
        self.nodes.add(node)
        
    def delNode(self, node):
        node.setParent(None)
        node.removeOwner()
        linkstodel = set()
        print "node to delete"
        print self.nodes
        print self.links
        for link in self.links :
            if (node is link.input) or (node is link.output):
                linkstodel.add(link)
        for link in linkstodel :
            self.delLink(link)         
        
        self.nodes.remove(node)
        
        print self.nodes
        print self.links
        
    def addLink(self, link):
        link.setParent(self)
        self.links.add(link)
    
    def delLink(self, link):
        link.setParent(None)
        link.removeOwner()
        link.input.delLink(link)
        self.disconnect(self.input, signalTransport, self.onAddPackage)
        self.disconnect(self, signalTransport, self.output.onPackageEntered)
        self.links.remove(link)
    
    def onNextTurnPressed(self):
        for player in self.players :
            player.onNextTurn()
    
    def openModel(self):
        pass
    
    def saveModel(self):
        pass
        
