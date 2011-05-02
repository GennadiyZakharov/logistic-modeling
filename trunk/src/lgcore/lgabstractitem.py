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
        self.cost = cost
        self.caption = caption
        self.owner = owner
        if owner is not None :
            self.connect(self, signalCost, owner.on_Cost)
        
    def on_NextTurn(self):
        if self.cost != 0 :
            self.emit(signalCost, self.cost)
         
        
