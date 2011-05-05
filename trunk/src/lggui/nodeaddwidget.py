from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgfactory import LgFactory
from lggui.factoryEditWidget import FactoryEditWidget


class NodeAddWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(NodeAddWidget, self).__init__(parent)
        
        layout = QtGui.QGridLayout()
        
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.textEdited.connect(self.on_updateText)
        nameText = QtGui.QLabel('Node name:')
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
        
        self.storageEdit = QtGui.QSpinBox()
        self.storageEdit.setMaximum(10)
        storageText = QtGui.QLabel('Storage Capacity:')
        layout.addWidget(storageText, 1, 0)
        layout.addWidget(self.storageEdit, 1, 1)
        
        self.factoryList = QtGui.QListWidget()
        layout.addWidget(self.factoryList, 2, 0, 2, 2)
        addfactoryButton = QtGui.QPushButton('Add Factory')
        addfactoryButton.clicked.connect(self.on_EditFactory)
        layout.addWidget(addfactoryButton, 4, 0)
        
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
        dialog = FactoryEditWidget(self)
        if dialog.exec_() :
            pass
        
        
