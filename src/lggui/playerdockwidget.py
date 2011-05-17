from PyQt4 import QtCore, QtGui

from lggui.playereditwidget import PlayerEditWidget

class PlayerDockWidget(QtGui.QWidget):
    def __init__(self, model, parent=None):
        super(PlayerDockWidget, self).__init__(parent)
        
        self.model = model
        #Slider and label
        layout = QtGui.QGridLayout()
        self.playerList = QtGui.QListWidget()
        layout.addWidget(self.playerList,0,0,1,2)
        self.addPlayerButton = QtGui.QPushButton('Add Player')
        self.addPlayerButton.clicked.connect(self.onAddPlayer)
        layout.addWidget(self.addPlayerButton,1,0)
        self.removePlayerButton = QtGui.QPushButton('Remove Player')
        self.removePlayerButton.clicked.connect(self.onRemovePlayer)
        layout.addWidget(self.removePlayerButton,1,1)
        self.editPlayerButton = QtGui.QPushButton('Edit Player')
        self.editPlayerButton.clicked.connect(self.onEditPlayer)
        layout.addWidget(self.editPlayerButton)
        
        self.setLayout(layout)
        
        self.onUpdateList()
        
    def onAddPlayer(self):
        dialog = PlayerEditWidget(None, self)
        if dialog.exec_():
            self.model.addPlayer(dialog.player)
            self.onUpdateList()
    
    def onRemovePlayer(self):
        if self.playerList.currentRow() == -1 :
            return
        self.onUpdateList()
    
    def onEditPlayer(self):
        if self.playerList.currentRow() == -1 :
            return
        self.onUpdateList()
    
    def onUpdateList(self):
        self.playerList.clear()
        for player in self.model.players :
            text = '{0:20} {1:10}'.format(player.name,player.money)
            self.playerList.addItem(text)
        