from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgfactory import LgFactory
from lgcore.lgnode import LgNode
from lggui.factoryEditWidget import FactoryEditWidget
from lggui.factorylistitem import FactoryListItem


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
        self.nameEdit.textEdited.connect(self.onNameChanged)
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
        addFactoryButton = QtGui.QPushButton('Add Factory')
        addFactoryButton.clicked.connect(self.onAddFactory)
        layout.addWidget(addFactoryButton, 4, 0)
        removeFactoryButton = QtGui.QPushButton('Remove Factory')
        removeFactoryButton.clicked.connect(self.onRemoveFactory)
        layout.addWidget(removeFactoryButton, 5, 0)
        editFactoryButton = QtGui.QPushButton('Edit Factory')
        editFactoryButton.clicked.connect(self.onEditFactory)
        layout.addWidget(editFactoryButton, 4, 1)
        
        self.onUpdateList()
        
        buttons = QtGui.QDialogButtonBox.Ok
        if node is None :
            buttons |= QtGui.QDialogButtonBox.Cancel
         
        self.buttonBox = QtGui.QDialogButtonBox(buttons)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        
        layout.addWidget(self.buttonBox, 6, 0, 1, 2)
        
        self.setLayout(layout)
        
    def onNameChanged(self, text):
        self.node.caption = text
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(text != '')
        
    def onStorageChamged(self, value):
        self.node.storageCapacity = value
        
    def onAddFactory(self):
        dialog = FactoryEditWidget(None, self)
        if dialog.exec_():
            self.node.addFactory(dialog.factory)
            self.onUpdateList()
    
    def onRemoveFactory(self):
        if self.factoryList.currentRow() == -1 :
            return
        factory = self.factoryList.currentItem().factory
        self.node.removeFactory(factory)
        self.onUpdateList()
    
    def onEditFactory(self):
        if self.factoryList.currentRow() == -1 :
            return
        dialog = FactoryEditWidget(self.factoryList.currentItem().factory)
        dialog.exec_()
        self.onUpdateList()
    
    def onUpdateList(self):
        self.factoryList.clear()
        for factory in self.node.factories :
            self.factoryList.addItem(FactoryListItem(factory))
            
    
        
        
        
