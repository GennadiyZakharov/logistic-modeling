from PyQt4 import QtCore, QtGui

class ToolsDockBar(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ToolsDockBar, self).__init__(parent)
        
        #Slider and label
        layout = QtGui.QHBoxLayout()
        self.videoSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        layout.addWidget(self.videoSlider)
        self.timeLabel = QtGui.QLabel('N/A')
        layout.addWidget(self.timeLabel)
        self.nextTurnButton = QtGui.QPushButton("Next Turn")
        layout.addWidget(self.nextTurnButton)

        self.setLayout(layout)
