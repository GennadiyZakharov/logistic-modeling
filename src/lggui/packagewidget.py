'''
Created on 09.03.2011

@author: Gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *
from qrc_resources import *

class PackageWidget(QtGui.QListWidgetItem):
    '''
    This is class for package. 
    It containes name, count and picture for
    '''


    def __init__(self,package):
        '''
        Constructor
        '''
            
        self.package = package
        self.caption = package.caption + ' ' + str(package.count)
        
        super(PackageWidget, self).__init__(self.caption)
        self.setIcon(QtGui.QIcon(package.icon))
        
        
        
        
        