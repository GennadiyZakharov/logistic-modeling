'''
Created on 17.02.2011

@author: gena
'''
from PyQt4 import QtCore
from lgcore.signals import *
from lgcore.lgpackage import LgPackage

from lgcore.lgabstractitem import LgAbstractItem

class LgNode(LgAbstractItem):
    '''
    classdocs
    '''


    def __init__(self,cost=0,caption='Node'):
        '''
        Constructor
        '''
        super(LgNode, self).__init__(cost)
        self.caption = caption
        self.entered = []
        self.destination = []
        self.storage = []
        
        # TEST:
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil',count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn(self.cost)
        
    def on_AcceptGood(self,good):
        pass
        