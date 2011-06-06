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
        self.setWindowTitle('Connect to server')
        
        self.addressEdit = QtGui.QLineEdit('localhost')
        addressText = QtGui.QLabel('server address:')
        addressText.setBuddy(self.addressEdit)
        layout.addWidget(addressText,0,0)
        layout.addWidget(self.addressEdit,0,1)
        
        self.portEdit = QtGui.QLineEdit('1234')
        portText = QtGui.QLabel('server port:')
        portText.setBuddy(self.portEdit)
        layout.addWidget(portText,1,0)
        layout.addWidget(self.portEdit,1,1)
        
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