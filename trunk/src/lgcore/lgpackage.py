'''
Created on 17.02.2011

@author: gena
'''
from PyQt4 import QtCore
from lgcore.signals import *

from lgcore.lgabstractitem import LgAbstractItem

class LgPackage(LgAbstractItem):
    '''
    classdocs
    '''


    def __init__(self,cost=0,):
        '''
        Constructor
        '''
        super(LgPackage, self).__init__(cost)
        
    