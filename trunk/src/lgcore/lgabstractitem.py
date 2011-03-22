from PyQt4 import QtCore
from lgcore.signals import signalCost

class LgAbstractItem(QtCore.QObject):
    '''Base class'''

    def __init__(self, cost=0):
        super(LgAbstractItem, self).__init__()        
        self.cost = cost
        
    def on_NextTurn(self):
        if self.cost != 0 :
            self.emit(signalCost, self.cost)
         
        
