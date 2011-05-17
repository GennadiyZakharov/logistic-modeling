from PyQt4 import QtCore
from lgcore.signals import signalCost
from lgcore.lgabstractitem import LgAbstractItem
from lgcore.lgpackage import LgPackage

class  LgFactory(LgAbstractItem):
    '''
    classdocs
    '''


    def __init__(self, parent=None, owner=None, caption='Factory', cost=0):
        '''
        Constructor
        '''
        super(LgFactory, self).__init__(parent, owner, caption, cost)
        self.activationInterval = 3
        self.currentTurn = self.activationInterval 
        self.consumes = 1
        self.produce = 0
        

    def execute(self, packagelist):
        # TODO: Add package type
        if self.currentTurn == 0:
            self.currentTurn = self.activationInterval
            for i in range(self.consumes):
                packagelist.pop()
            
            for i in range(self.produce):
                packagelist.append(LgPackage(self.parent(), self.owner))

    def on_NextTurn(self, packagelist):
        self.currentTurn -= 1
        self.execute(packagelist)
        
        
