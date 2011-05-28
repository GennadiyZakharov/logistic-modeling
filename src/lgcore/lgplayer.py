from PyQt4 import QtCore
from hashlib import sha512
from lgcore.signals import signalNextTurnLink, signalNextTurn
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
        
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return self.kind + ' ' + self.name
    
    def onCost(self, value):
        self.money += value
        
    def onNextTurn(self):
        self.emit(signalNextTurnLink)
        self.emit(signalNextTurn)
        
        