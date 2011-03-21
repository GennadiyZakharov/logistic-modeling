'''
Created on 17.02.2011

@author: gena
'''
from hashlib import sha512
from PyQt4 import QtCore
from lgcore.signals import *

from lgcore.lgabstractitem import LgAbstractItem
from time import time

class LgPackage(LgAbstractItem):
    '''
    This is class for package
    '''

    def __init__(self,cost=0,caption='product',count=1,icon=':/penguin.png'):
        '''
        Constructor
        '''
        super(LgPackage, self).__init__(cost)
        self.caption = caption
        self.count = count
        self.icon = icon
        self.hashValue = int(sha512(str(time())).hexdigest(), 16) 
        
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return 'Package' + str(self.hashValue)
    