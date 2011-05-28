from hashlib import sha512
from time import time
import random

from PyQt4 import QtCore
from lgcore.signals import signalCost, signalNextTurn

class LgAbstractItem(QtCore.QObject):
    '''Base class'''

    def __init__(self, name, parent=None, cost=0, owner=None):
        '''
        owner -- player, who can manage this item
        parent -- usually lgsheme
        cost -- use cost per turn
        '''
        super(LgAbstractItem, self).__init__(parent)     
        
        self.hashValue = int(sha512(str(time() + random.randint(0, 100))).hexdigest(), 16)
        
        self.kind = 'AbstractItem'
        self.name = name
        self.cost = cost
        self.pos = QtCore.QPointF(10,10)
        self.owner = None
        if owner is not None :
            self.setOwner(owner)
        self.viewers = set()      
            
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return self.kind + ' ' + self.name
        
    def setOwner(self, owner=None, signal=signalNextTurn):
        if self.owner is not None :
            self.disconnect(self, signalCost, self.owner.onCost)
            self.disconnect(self.owner, signal, self.onNextTurn)
        self.owner = owner
        if self.owner is not None :
            self.connect(self, signalCost, self.owner.onCost)
            self.connect(self.owner, signal, self.onNextTurn)
        
    #--------------------------------------------------------
    def onNextTurn(self):
        if self.cost != 0 :
            self.emit(signalCost, self.cost)
         
        
