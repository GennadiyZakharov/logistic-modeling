'''
Created on 08.03.2011

@author: Gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

from lggui.packagewidget import PackageWidget

class NodeWidget(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(NodeWidget, self).__init__(parent)
        
        inputLabel = QtGui.QLabel('To sorting')
        
        self.inputList = QtGui.QListWidget()
        self.inputList.setAcceptDrops(True)
        self.inputList.setDragEnabled(True)
        self.inputList.dropAction = QtCore.Qt.MoveAction
        inputLabel.setBuddy(self.inputList)
        
        layout = QtGui.QGridLayout()
        layout.addWidget(inputLabel, 0, 0)
        layout.addWidget(self.inputList, 1, 0)
        self.setLayout(layout)
        
        item = PackageWidget('Good 1')
        
        self.inputList.addItem(item)
        
        
        
        


        