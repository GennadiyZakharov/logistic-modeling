'''
Created on 04.02.2011

@author: gena
'''
from PyQt4 import QtCore
from lgcore.signals import *

from lgcore.lgabstractitem import LgAbstractItem

class LgLink(LgAbstractItem):
    '''
    This class implements all functionality for link
    '''

    def __init__(self,cost=0,length=1):
        '''
        Constructor
        '''
        super(LgLink, self).__init__(cost)
        self.length = length
        self.goods = [] # List for store goods
        #self.dist = []
        
    def on_NextTurn(self):
        super(LgLink, self).on_NextTurn()
        for good,age in self.goods :
            if age == 0 :
                #self.emit()
                self.goods.remove((good,age))
            # decrease by one age of good
                
        
    def on_addPackage(self,package):
        '''
        Add new package to transport
        '''
        self.goods.append((package,0))
        
        