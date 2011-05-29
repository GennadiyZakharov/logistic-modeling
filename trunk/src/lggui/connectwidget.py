from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgplayer import LgPlayer

class ConnectWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, player=None, parent=None):
        '''
        Constructor
        '''
        super(ConnectWidget, self).__init__(parent)
        
        layout = QtGui.QGridLayout()
        self.setWindowTitle('Edit player properties')
        
        self.nameEdit = QtGui.QLineEdit('')
        nameText = QtGui.QLabel('server address:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText,0,0)
        layout.addWidget(self.nameEdit,0,1)
        
        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.clicked.connect(self.onConnect)
        layout.addWidget(self.connectButton,0,2)
        
        self.playerEdit = QtGui.QComboBox()
        self.playerEdit.currentIndexChanged.connect(self.onSelectPlayer)
        playerText = QtGui.QLabel('Player:')
        playerText.setBuddy(self.playerEdit)
        layout.addWidget(playerText,1,0)
        layout.addWidget(self.playerEdit,1,1)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.setLayout(layout)
    
    def onConnect(self):
        dialog = QtGui.QProgressDialog()
        dialog.show()
    
    def onSelectPlayer(self):
        pass