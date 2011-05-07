
from PyQt4 import QtCore

from lgcore.lgplayer import LgPlayer
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage

from lgcore.signals import *


class LgScheme(QtCore.QObject):
    '''
    This is holder class for all logistic system
    It contains all nodes, links and packages
    
    It also  containes all payed data
    '''
    def __init__(self):
        super(LgScheme, self).__init__()
        self.players = set()
        self.teacher = LgPlayer('Teacher',self)
        self.players.add(self.teacher)
        self.links = set()
        self.nodes = set()
        #self.packages = []
    
    def addNode(self, owner=None, caption='Node', storageCapacity=10, cost=0):
        node = LgNode(self, owner, caption, storageCapacity, cost)
        self.nodes.add(node)
        self.connect(self, signalNextTurnNode, node.on_NextTurn)
        return node
        
    def addLink(self, input, output, owner=None, caption='Link', 
                length=5, maxCapacity=5, cost=0):
        link = LgLink(input, output, self, owner, caption, 
                      length, maxCapacity, cost)
        self.links.add(link)
        self.connect(self, signalNextTurnLink, link.on_NextTurn)
        return link
    
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
    
    
    def openScheme(self):
        pass
    
    def saveScheme(self):
        pass
        
