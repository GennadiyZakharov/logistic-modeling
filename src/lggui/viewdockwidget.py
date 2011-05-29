from PyQt4 import QtCore, QtGui

class ViewDockWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ViewDockWidget, self).__init__(parent)
        
        #Slider and label
        layout = QtGui.QHBoxLayout()
        self.zoomSpinBox = QtGui.QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        zoomLabel = QtGui.QLabel('Zoom:')
        zoomLabel.setBuddy(self.zoomSpinBox)
        layout.addWidget(zoomLabel)
        layout.addWidget(self.zoomSpinBox)

        self.setLayout(layout)
