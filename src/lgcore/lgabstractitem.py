'''
Created on 04.02.2011

@author: gena
'''

from PyQt4 import QtCore
from lgcore.signals import *

class LgAbstractItem(QtCore.QObject):
    '''
    This is base class for all 
    '''


    def __init__(self,cost=0):
        '''
        Constructor
        '''
        self.cost = cost #Cost per turn
        
    def on_NextTurn(self):
        self.emit(signalCost,self.cost)
         
        