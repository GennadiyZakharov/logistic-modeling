'''
Created on 08.03.2011

@author: Gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

from lggui.packagewidget import PackageWidget
from lggui.dndmenuListwidget import DnDMenuListWidget
from lggui.dndtablewidget import DnDTableWidget

class NodeWidget(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(NodeWidget, self).__init__(parent)
        
        inputLabel = QtGui.QLabel('Input Packages')
        outputLabel = QtGui.QLabel('To sorting')
        self.inputList = DnDMenuListWidget()
        self.outputList = DnDTableWidget()
        inputLabel.setBuddy(self.inputList)
        outputLabel.setBuddy(self.outputList)
        
        storageLabel = QtGui.QLabel('Storage')
        self.storageList = DnDMenuListWidget()
        storageLabel.setBuddy(self.storageList)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(inputLabel, 0, 0)
        layout.addWidget(outputLabel, 0, 1)
        layout.addWidget(self.inputList, 1, 0)
        layout.addWidget(self.outputList, 1, 1)
        
        layout.addWidget(storageLabel, 2, 0, 1, 2)
        layout.addWidget(self.storageList, 3, 0, 1, 2)
        
        self.setLayout(layout)
        
        item = PackageWidget('Good 1')
        
        self.inputList.addItem(item)
        
        
        
        


        