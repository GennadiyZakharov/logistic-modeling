from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgplayer import LgPlayer

class PlayerEditWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, player=None, parent=None):
        '''
        Constructor
        '''
        super(PlayerEditWidget, self).__init__(parent)
        
        self.player = player if player is not None else LgPlayer('root')
        
        layout = QtGui.QGridLayout()
        self.setWindowTitle('Edit player properties')
        
        self.nameEdit = QtGui.QLineEdit(self.player.name)
        self.nameEdit.textEdited.connect(self.onUpdateName)
        nameText = QtGui.QLabel('Player name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
         
        self.moneyEdit = QtGui.QSpinBox()
        self.moneyEdit.setMaximum(10000)
        self.moneyEdit.setValue(self.player.money)
        self.moneyEdit.valueChanged.connect(self.onUpdateMoney)
        moneyText = QtGui.QLabel('Money:')
        moneyText.setBuddy(self.moneyEdit)
        layout.addWidget(moneyText, 1, 0)
        layout.addWidget(self.moneyEdit, 1, 1)
        
        buttons = QtGui.QDialogButtonBox.Ok
        if player is None :
            buttons |= QtGui.QDialogButtonBox.Cancel
        
        self.buttonBox = QtGui.QDialogButtonBox(buttons)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        
        layout.addWidget(self.buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)
    
    
    def onUpdateName(self, text):
        self.player.name = text
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(text != '')
        
    def onUpdateMoney(self, value):
        self.player.money = value
