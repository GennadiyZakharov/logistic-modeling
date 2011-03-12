'''
Created on 17.02.2011

@author: gena
'''
from PyQt4 import QtCore
from lgcore.signals import *

from lgcore.lgabstractitem import LgAbstractItem

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
        
    