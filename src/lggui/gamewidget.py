from PyQt4 import QtCore, QtGui

class GameWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(GameWidget, self).__init__(parent)
        
        #Slider and label
        layout = QtGui.QHBoxLayout()
        
        self.turnLabel = QtGui.QLabel('Turn: N/A')
        layout.addWidget(self.turnLabel)
        self.nextTurnButton = QtGui.QPushButton("End Turn")
        layout.addWidget(self.nextTurnButton)

        self.setLayout(layout)
        
    def onNextTurn(self, turn):
        self.turnLabel.setText('Turn: {0}'.format(turn))
        
