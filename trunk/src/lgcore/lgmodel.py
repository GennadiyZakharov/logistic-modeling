
from PyQt4 import QtCore

from lgcore.lgplayer import LgPlayer
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage

from lgcore.signals import *

class LgModel(QtCore.QObject):
    '''
    This is holder class for all logistic system
    It contains all nodes, links and packages
    
    It also  containes all payed data
    '''
    def __init__(self):
        super(LgModel, self).__init__()
        self.players = set()
        self.teacher = LgPlayer('Teacher',self)
        self.players.add(self.teacher)
        self.links = set()
        self.nodes = set()
        self.packages = set()
    
    def addPlayer(self, player):
        self.players.add(player)
    
    def delPlayer(self, player):
        self.players.remove(player)
    
    def addNode(self, node):
        node.setParent(self)
        self.nodes.add(node)
        self.connect(self, signalNextTurnNode, node.on_NextTurn)
        
    def addLink(self, link):
        link.setParent(self)
        self.links.add(link)
        self.connect(self, signalNextTurnLink, link.on_NextTurn)
    
    def delLink(self, link):
        self.link.input.delLink(link)
        self.links.remove(link)
        
    def delNode(self, node):
        for link in self.links :
            if (node is link.input) or (node is link.output):
                self.delLink(link)
        self.nodes.remove(node)
    
    def on_NextTurnPressed(self):
        self.emit(signalNextTurnLink) # Move all packages trough links
        self.emit(signalNextTurnNode)
    
    
    def openModel(self):
        pass
    
    def saveModel(self):
        pass
        
