from PyQt4 import QtGui
from lgcore.lgabstractitem import LgAbstractItem
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalTransport, signalNextTurnLink, signalUpdateGui, \
    signalCost

class LgLink(LgAbstractItem):
    '''This class implements all functionality for link '''

    def __init__(self, input, output, name='Link', parent=None, cost=0, owner=None,
                 length=5, maxCapacity=5):
        super(LgLink, self).__init__(name, parent, cost, owner)
        
        self.kind = 'Link'
        self.input = input
        self.output = output
        self.length = length
        self.color = QtGui.QColor(205, 235, 139)
        self.maxCapacity = maxCapacity
        self.currentCapacity = self.maxCapacity
        self.packages = {} # Dictionary for store packages
        
        self.input.addLink(self)
        
        self.connect(self.input, signalTransport, self.onAddPackage)
        self.connect(self, signalTransport, self.output.onPackageEntered)
    
    def updateData(self):
        self.emit(signalUpdateGui)
    
    def setOwner(self, owner):
        super(LgLink, self).setOwner(owner, signal=signalNextTurnLink)
    
    def onNextTurn(self):
        for p in self.packages.keys():
            self.packages[p] -= 1
            if self.packages[p] == 0 :
                del self.packages[p]
                self.emit(signalTransport, p)
            # decrease by one age of good
        self.currentCapacity = self.maxCapacity
        self.emit(signalUpdateGui)
          
        
    def onAddPackage(self, package):
        '''Add new package to transport'''
        if self.currentCapacity > 0:
            self.packages[package] = self.length
            self.currentCapacity -= 1
            self.emit(signalCost, -self.cost)
            self.emit(signalUpdateGui)
        else:
            raise ValueError('Max capacity of link exceeded!')
        
        
