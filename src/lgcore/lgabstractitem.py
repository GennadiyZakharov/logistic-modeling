from hashlib import sha512
from time import time
import random

from PyQt4 import QtCore
from lgcore.signals import signalCost

class LgAbstractItem(QtCore.QObject):
    '''Base class'''

    def __init__(self, parent=None, owner=None, caption='Item', cost=0):
        '''
        owner -- player, who can manage this item
        parent -- usually lgsheme
        cost -- use cost per turn
        '''
        super(LgAbstractItem, self).__init__(parent)     
        self.hashValue = int(sha512(str(time() + random.randint(0, 100))).hexdigest(), 16)
           
        self.cost = cost
        self.caption = caption
        self.owner = owner
        if owner is not None :
            self.connect(self, signalCost, owner.on_Cost)
        # TODO: Add viewers        
            
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return 'AbstractItem' + str(self.hashValue)
        
    def on_NextTurn(self):
        if self.cost != 0 :
            self.emit(signalCost, self.cost)
         
        
