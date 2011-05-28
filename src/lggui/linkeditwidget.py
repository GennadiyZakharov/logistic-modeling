from PyQt4 import QtGui, QtCore
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.signals import *
from lggui.linkaddwidget import LinkAddWidget
from lggui.playerlistitem import PlayerListItem


class LinkEditWidget(QtGui.QDialog):
    '''
    This is widget to edit link
    '''


    def __init__(self, model, link, parent=None):
        '''
        Constructor
        '''
        super(LinkEditWidget, self).__init__(parent)
        self.model = model
        
        self.link = link
        
        layout = QtGui.QGridLayout()
        
        self.setWindowTitle('Edit link properties')

        self.nameEdit = QtGui.QLineEdit(self.link.name)
        self.nameEdit.textEdited.connect(self.onNameChanged)
        nameText = QtGui.QLabel('Link name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
        
        self.ownerEdit = QtGui.QComboBox()
        self.ownerEdit.addItem('<None>')
        print model.players
        for player in model.players :
            self.ownerEdit.addItem(player.name)
            
        if self.link.owner is not None :
            self.ownerEdit.setCurrentIndex(model.players.index(self.link.owner)+1)
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
            if player in self.link.viewers :
                playerItem.setSelected(True)
        #----
        self.viewersEdit.itemSelectionChanged.connect(self.onViewersChanged)
        viewersText = QtGui.QLabel('Viewers:')
        viewersText.setBuddy(self.viewersEdit)
        layout.addWidget(viewersText, 2, 0)
        layout.addWidget(self.viewersEdit, 3, 0, 1, 2)
        
        self.lengthEdit = QtGui.QSpinBox()
        self.lengthEdit.setMaximum(10)
        self.lengthEdit.setValue(self.link.length)
        self.lengthEdit.valueChanged.connect(self.onLengthChanged)
        lengthText = QtGui.QLabel('Length:')
        lengthText.setBuddy(self.lengthEdit)
        layout.addWidget(lengthText, 5, 0)
        layout.addWidget(self.lengthEdit, 5, 1)
        
        self.capacityEdit = QtGui.QSpinBox()
        self.capacityEdit.setMaximum(10)
        self.capacityEdit.setValue(self.link.maxCapacity)
        self.capacityEdit.valueChanged.connect(self.onCapacityChanged)
        capacityText = QtGui.QLabel('Capacity:')
        capacityText.setBuddy(self.capacityEdit)
        layout.addWidget(capacityText, 6, 0)
        layout.addWidget(self.capacityEdit, 6, 1)
        
        colorButton = QtGui.QPushButton('Select Color')
        layout.addWidget(colorButton, 11, 1)
        colorButton.clicked.connect(self.onSelectColor)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        layout.addWidget(self.buttonBox, 15, 0, 1, 2)
        
        self.setLayout(layout)
        
    def onNameChanged(self, text):
        self.link.name = str(text)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(text != '')
        
    def onLengthChanged(self, value):
        self.link.length = value
            
    def onCapacityChanged(self, value):
        self.link.maxCapacity = value
            
    def onSelectColor(self):
        colorEdit = QtGui.QColorDialog(self)
        colorEdit.setCurrentColor(self.link.color)
        if colorEdit.exec_() :
            self.link.color = colorEdit.currentColor()
            
    def onOwnerChanged(self, index):
        if index !=0 :
            self.link.setOwner(self.model.players[index-1])
        else:
            self.link.setOwner(None)
        
    def onViewersChanged(self):
        self.link.viewers.clear()
        for item in self.viewersEdit.selectedItems() : 
            self.link.viewers.add(item.player)
        
        
        
        
