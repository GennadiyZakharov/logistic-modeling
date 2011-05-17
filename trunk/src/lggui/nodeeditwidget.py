from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgfactory import LgFactory
from lgcore.lgnode import LgNode
from lggui.factoryEditWidget import FactoryEditWidget


class NodeEditWidget(QtGui.QDialog):
    '''
    This is widget to create/edit new node
    '''


    def __init__(self, node=None, parent=None):
        '''
        Constructor
        '''
        super(NodeEditWidget, self).__init__(parent)
        
        self.node = node if node is not None else LgNode()
        
        layout = QtGui.QGridLayout()
        
        self.nameEdit = QtGui.QLineEdit(self.node.caption)
        self.nameEdit.textEdited.connect(self.on_updateText)
        nameText = QtGui.QLabel('Node name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
        
        self.storageEdit = QtGui.QSpinBox()
        self.storageEdit.setValue(self.node.storageCapacity)
        self.storageEdit.setMaximum(10)
        storageText = QtGui.QLabel('Storage Capacity:')
        storageText.setBuddy(self.storageEdit)
        layout.addWidget(storageText, 1, 0)
        layout.addWidget(self.storageEdit, 1, 1)
        
        self.factoryList = QtGui.QListWidget()
        layout.addWidget(self.factoryList, 2, 0, 2, 2)
        addfactoryButton = QtGui.QPushButton('Add Factory')
        addfactoryButton.clicked.connect(self.on_EditFactory)
        layout.addWidget(addfactoryButton, 4, 0)
        # TODO: read information about factories 
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.setLayout(layout)
        
        
        
    def on_updateText(self, text):
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(text != '')
        
    def on_EditFactory(self):
        #if
        dialog = FactoryEditWidget(None, self)
        
        if dialog.exec_() :
            print dialog.factory
        
        
