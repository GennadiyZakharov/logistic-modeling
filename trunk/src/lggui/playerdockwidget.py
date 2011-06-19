from PyQt4 import QtCore, QtGui

from lggui.playereditwidget import PlayerEditWidget
from lggui.playerlistitem import PlayerListItem
from lggui.lggraph import LgGraph
import matplotlib.pyplot as plt

class PlayerDockWidget(QtGui.QWidget):
    
    tempFileName = 'tempgraph.png'
    def __init__(self, model, parent=None, edit=True):
        super(PlayerDockWidget, self).__init__(parent)
        
        self.model = model
        #Slider and label
        layout = QtGui.QGridLayout()
        self.playerList = QtGui.QListWidget()
        layout.addWidget(self.playerList, 0, 0, 1, 2)
        if edit :
            self.addPlayerButton = QtGui.QPushButton('Add Player')
            self.addPlayerButton.clicked.connect(self.onAddPlayer)
            layout.addWidget(self.addPlayerButton, 1, 0)
            self.removePlayerButton = QtGui.QPushButton('Remove Player')
            self.removePlayerButton.clicked.connect(self.onRemovePlayer)
            layout.addWidget(self.removePlayerButton, 1, 1)
            self.editPlayerButton = QtGui.QPushButton('Edit Player')
            self.editPlayerButton.clicked.connect(self.onEditPlayer)
            layout.addWidget(self.editPlayerButton, 2, 0)
        self.graphLabel = QtGui.QLabel('Graph')
        self.playerList.currentRowChanged.connect(self.onUpdateGraph)
        #self.playerList.cu
        layout.addWidget(self.graphLabel, 3, 0, 1, 2)
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
        player = self.playerList.currentItem().player
        self.model.delPlayer(player)
        self.onUpdateList()
    
    def onEditPlayer(self):
        if self.playerList.currentRow() == -1 :
            return
        dialog = PlayerEditWidget(self.playerList.currentItem().player)
        dialog.exec_()
        self.onUpdateList()
    
    def onUpdateList(self):
        self.playerList.clear()
        for player in self.model.players :
            self.playerList.addItem(PlayerListItem(player))
    
    def onUpdateGraph(self):
        if self.playerList.currentRow() == -1 :
            
            self.graphLabel.setText('graph')
            return
        player = self.playerList.currentItem().player
        graphData = [income - cost for cost, income in player.balanceHistory]
        if graphData == []:
            return 
        #graph = LgGraph() 
        plt.close('all')
        F = plt.figure(figsize=(4,4), dpi=72)
        ax = F.add_subplot(111)
        ax.set_title(player.name + ' balance')
        ax.set_xlabel('Turn')
        ax.format_xdata = lambda x: "1-{0}".format(x) 
        ax.set_ylabel('Money')
        ax.plot(graphData)
        F.savefig(self.tempFileName, dpi=72)
        
        image = QtGui.QImage(self.tempFileName)
        if image.isNull():
            print "Failed to read {0}".format(self.tempFileName)
        else:
            self.graphLabel.setPixmap(QtGui.QPixmap.fromImage(image))



        

        
