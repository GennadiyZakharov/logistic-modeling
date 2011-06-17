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
            layout.addWidget(self.editPlayerButton)
        self.graphLabel = QtGui.QLabel('Graph')
        self.playerList.currentRowChanged.connect(self.onUpdateGraph)
        #self.playerList.cu
        layout.addWidget(self.graphLabel, 2, 0, 1, 2)
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
        graph = LgGraph() 
        #graph.setTitle(player.name + ' balance')
        #graph.setXLabel('Turn')
        #graph.setYLabel('Money')
        print player.name,graphData
        #graph.plotGraph({'pl1':graphData, 'pl2':graphData}, 'graph.png')
        # TODO: FixMe
        plt.plot([1,2,3,4,5],[9,8,7,6,5])
        
        image = QtGui.QImage(self.tempFileName)
        if image.isNull():
            print "Failed to read {0}".format(fname)
        else:
            self.graphLabel.setPixmap(QtGui.QPixmap.fromImage(image))



        

        
