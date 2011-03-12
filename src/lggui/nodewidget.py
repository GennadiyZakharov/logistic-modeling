'''
Created on 08.03.2011

@author: Gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *
from lgcore.lgpackage import LgPackage

from lggui.packagewidget import PackageWidget
from lggui.dndmenuListwidget import DnDMenuListWidget
from lggui.dndtablewidget import DnDTableWidget

class NodeWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self,node,parent=None):
        '''
        Constructor
        '''
        super(NodeWidget, self).__init__(parent)
        
        self.node = node # This is link to core node, wich represents
            # all node functionality 
        
        self.setWindowTitle(self.node.caption)
         
        inputLabel = QtGui.QLabel('Come:')
        outputLabel = QtGui.QLabel('Destination:')
        self.inputList = DnDMenuListWidget(self)
        self.outputList = DnDTableWidget(self)
        inputLabel.setBuddy(self.inputList)
        outputLabel.setBuddy(self.outputList)
        storageLabel = QtGui.QLabel('Storage:')
        self.storageList = DnDMenuListWidget(self)
        storageLabel.setBuddy(self.storageList)
        
        self.okBtn = QtGui.QPushButton('&OK')
        self.connect(self.okBtn, signalClicked,self.accept)
                      
        layout = QtGui.QGridLayout()
        layout.addWidget(inputLabel, 0, 0)
        layout.addWidget(outputLabel, 0, 1)
        layout.addWidget(self.inputList, 1, 0)
        layout.addWidget(self.outputList, 1, 1)
        
        layout.addWidget(storageLabel, 2, 0, 1, 2)
        layout.addWidget(self.storageList, 3, 0, 1, 2)
        layout.addWidget(self.okBtn, 4, 1)
        
        #vSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
       
        self.setLayout(layout)
        
        for package in node.entered :
            item = PackageWidget(package)
            self.inputList.addItem(item)
            
        for package in node.storage :
            item = PackageWidget(package)
            self.storageList.addItem(item)
        '''    
        for package in node.storage :
            item = PackageWidget(package)
            self.storageList.addItem(item)
        ''' 
        
        
        
        
        


        