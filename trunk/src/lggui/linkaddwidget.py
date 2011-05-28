from PyQt4 import QtGui, QtCore
from lgcore.lgnode import LgNode
from lgcore.signals import *
from lggui.factoryEditWidget import FactoryEditWidget
from lggui.factorylistitem import FactoryListItem
from lggui.playerlistitem import PlayerListItem

class LinkAddWidget(QtGui.QDialog):
    '''
    This is widget to create/edit new node
    '''


    def __init__(self, model, parent=None):
        '''
        Constructor
        '''
        super(LinkAddWidget, self).__init__(parent)
        self.model = model
        
        self.nodesList = []
        self.nodesNames = []
        for node in model.nodes :
            self.nodesList.append(node)
            self.nodesNames.append(node.name)
        
        layout = QtGui.QGridLayout()
        
        self.setWindowTitle('Create New link')
        
        self.inputEdit = QtGui.QComboBox()
        inputText = QtGui.QLabel('Input node:')
        inputText.setBuddy(self.inputEdit)
        layout.addWidget(inputText, 0, 0)
        layout.addWidget(self.inputEdit, 1, 0)
        
        self.outputEdit = QtGui.QComboBox()
        outputText = QtGui.QLabel('Outnput node:')
        outputText.setBuddy(self.outputEdit)
        layout.addWidget(outputText, 0, 1)
        layout.addWidget(self.outputEdit, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        #self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        layout.addWidget(self.buttonBox, 15, 0, 1, 2)
        
        
        self.populate(self.inputEdit)
        self.inputEdit.currentIndexChanged.connect(self.onItemChanged)
        self.outputEdit.currentIndexChanged.connect(self.onItemChanged)
        self.populate(self.outputEdit)
        
        self.setLayout(layout)
        
    def populate(self, comboBox):
        for name in self.nodesNames :
            comboBox.addItem(name)
        
    def onItemChanged(self):
        flag = (self.inputEdit.currentIndex() != self.outputEdit.currentIndex())
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(flag)
        
    def accept(self):
        self.input  = self.nodesList[ self.inputEdit.currentIndex()]
        self.output = self.nodesList[self.outputEdit.currentIndex()]
        return super(LinkAddWidget, self).accept()
        

