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

    def __init__(self,input,output,cost=0,length=1):
        '''
        Constructor
        '''
        super(LgLink, self).__init__(cost)
        
        self.input  = input
        self.output = output
        self.length = length
        self.packages = [] # List for store packages
        
        self.input.addLink(self)
        
        self.connect(self.input,signalTransport,self.on_addPackage)
        self.connect(self,signalTransport,self.output.on_PackageEntered)
        
    def on_NextTurn(self):
        super(LgLink, self).on_NextTurn()
        for item in self.packages :
            item[1] -= 1
            if item[1] == 0 :
                self.emit(signalTransport,item[0])
                self.remove(item)
            # decrease by one age of good
                
        
    def on_addPackage(self,package):
        '''
        Add new package to transport
        '''
        self.packages.append([package,self.length])
        
        