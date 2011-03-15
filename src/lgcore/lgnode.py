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
    This is class for logistic node. It can produce, consume and 
    distribute products for several links
    '''


    def __init__(self,cost=0,caption='Node'):
        '''
        Constructor
        '''
        super(LgNode, self).__init__(cost)
        
        self.caption = caption
        # List of links, to which product will be distributed
        self.links = []
        
        # lists for all products
        self.entered = [] # products to be distributed
        self.storage = [] # storage to store products for a several time
        
        # TEST:
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil',count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        
    def addLink(self,link):
        self.links.append(link)
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn(self.cost)        
        
    def on_PackageEntered(self,package):
        self.entered.append(package)
        