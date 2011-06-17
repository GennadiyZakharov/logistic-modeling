from PyQt4 import QtCore
from hashlib import sha512
from lgcore.signals import signalNextTurnLink, signalPlayerTurn
from time import time
import random


class LgPlayer(QtCore.QObject):
    '''
    classdocs
    '''

    def __init__(self, name, parent=None, money=0):
        '''
        Constructor
        '''
        super(LgPlayer, self).__init__(parent)
        self.hashValue = int(sha512(str(time() + random.randint(0, 100))).hexdigest(), 16)
        
        self.kind = 'Player'
        self.name = name
        self.money = money
        self.currentIncome = 0
        self.currentCost = 0
        self.balanceHistory = []
        
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return self.kind + ' ' + self.name
    
    def onCost(self, value):
        self.money += value
        if value > 0 :
            self.currentIncome += value
        else:
            self.currentCost -= value
        
    def onTurn(self):
        self.emit(signalPlayerTurn)
        self.balanceHistory.append((self.currentCost,
                                    self.currentIncome))
        self.currentCost = 0
        self.currentIncome = 0
        