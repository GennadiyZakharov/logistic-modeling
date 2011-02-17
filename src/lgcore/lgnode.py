'''
Created on 17.02.2011

@author: gena
'''
from PyQt4 import QtCore
from lgcore.signals import *

from lgcore.lgabstractitem import LgAbstractItem

class LgNode(LgAbstractItem):
    '''
    classdocs
    '''


    def __init__(self,cost=0):
        '''
        Constructor
        '''
        super(LgNode, self).__init__(cost)
        links = []
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn(self.cost)
        
    def on_AcceptGood(self,good):
        pass
        