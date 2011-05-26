from PyQt4 import QtGui, QtCore
from lgcore.lgnode import LgNode
from lgcore.signals import *
from lggui.factoryEditWidget import FactoryEditWidget
from lggui.factorylistitem import FactoryListItem
from lggui.playerlistitem import PlayerListItem




class NodeEditWidget(QtGui.QDialog):
    '''
    This is widget to create/edit new node
    '''


    def __init__(self, model, node=None, parent=None):
        '''
        Constructor
        '''
        super(NodeEditWidget, self).__init__(parent)
        self.model = model
        self.node = node if node is not None else LgNode()
        
        layout = QtGui.QGridLayout()
        
        self.setWindowTitle('Edit node properties')
        
        self.nameEdit = QtGui.QLineEdit(self.node.name)
        self.nameEdit.textEdited.connect(self.onNameChanged)
        nameText = QtGui.QLabel('Node name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
        
        self.ownerEdit = QtGui.QComboBox()
        self.ownerEdit.addItem('<None>')
        print model.players
        for player in model.players :
            self.ownerEdit.addItem(player.name)
            
        if self.node.owner is not None :
            self.ownerEdit.setCurrentIndex(model.players.index(self.node.owner)+1)
        else :
            self.ownerEdit.setCurrentIndex(0)
        self.ownerEdit.currentIndexChanged.connect(self.onOwnerChanged)
        ownerText = nameText = QtGui.QLabel('Owner:')
        ownerText.setBuddy(self.ownerEdit)
        layout.addWidget(self.ownerEdit, 1, 1)
        layout.addWidget(ownerText, 1, 0)
        
        self.viewersEdit = QtGui.QListWidget()
        self.viewersEdit.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for player in model.players :
            playerItem = PlayerListItem(player)
            self.viewersEdit.addItem(playerItem)
            if player in self.node.viewers :
                playerItem.setSelected(True)
        #----
        self.viewersEdit.itemSelectionChanged.connect(self.onViewersChanged)
        viewersText = QtGui.QLabel('Viewers:')
        viewersText.setBuddy(self.viewersEdit)
        layout.addWidget(viewersText, 2, 0)
        layout.addWidget(self.viewersEdit, 3, 0, 1, 2)
        
        self.storageEdit = QtGui.QSpinBox()
        self.storageEdit.setValue(self.node.storageCapacity)
        self.storageEdit.setMaximum(10)
        storageText = QtGui.QLabel('Storage Capacity:')
        storageText.setBuddy(self.storageEdit)
        layout.addWidget(storageText, 5, 0)
        layout.addWidget(self.storageEdit, 5, 1)
        
        self.factoryList = QtGui.QListWidget()
        layout.addWidget(self.factoryList, 7, 0, 2, 2)
        addFactoryButton = QtGui.QPushButton('Add Factory')
        addFactoryButton.clicked.connect(self.onAddFactory)
        layout.addWidget(addFactoryButton, 10, 0)
        removeFactoryButton = QtGui.QPushButton('Remove Factory')
        removeFactoryButton.clicked.connect(self.onRemoveFactory)
        layout.addWidget(removeFactoryButton, 11, 0)
        editFactoryButton = QtGui.QPushButton('Edit Factory')
        editFactoryButton.clicked.connect(self.onEditFactory)
        layout.addWidget(editFactoryButton, 10, 1)
        
        colorButton = QtGui.QPushButton('Select Color')
        layout.addWidget(colorButton, 11, 1)
        colorButton.clicked.connect(self.onSelectColor)
        
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
        layout.addWidget(self.buttonBox, 15, 0, 1, 2)
        
        self.setLayout(layout)
        
    def onNameChanged(self, text):
        self.node.name = text
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
            
    def onSelectColor(self):
        colorEdit = QtGui.QColorDialog(self)
        colorEdit.setCurrentColor(self.node.color)
        if colorEdit.exec_() :
            self.node.color = colorEdit.currentColor()
            
    def onOwnerChanged(self, index):
        print index
        if index !=0 :
            self.node.setOwner(self.model.players[index-1])
        else:
            self.node.setOwner(None)
        
    def onViewersChanged(self):
        self.node.viewers.clear()
        for item in self.viewersEdit.selectedItems() : 
            self.node.viewers.add(item.player)
        
        
        
        
