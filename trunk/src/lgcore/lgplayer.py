from hashlib import sha512
from time import time
import random

from PyQt4 import QtCore

class LgPlayer(QtCore.QObject):
    '''
    classdocs
    '''


    def __init__(self, name, parent=None):
        '''
        Constructor
        '''
        super(LgPlayer, self).__init__(parent)
        self.hashValue = int(sha512(str(time() + random.randint(0, 100))).hexdigest(), 16)
        
        self.kind = 'Player'
        self.name = name
        self.money = 1000
        
    def on_Cost(self, value):
        self.money += value
        
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return self.kind + ' ' + self.caption + ' ' + str(self.hashValue)
        
        