'''
Created on Mar 21, 2011

@author: mk
'''
from PyQt4 import QtCore
from lgcore.signals import *

class LgScheme(QtCore.QObject):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(LgScheme, self).__init__()
        
    def on_NextTurnPressed(self):
        self.emit(signalNextTurn)
        