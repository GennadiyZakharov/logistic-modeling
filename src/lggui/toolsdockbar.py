'''
Created on 25.01.2011

@author: gena
'''
from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

class ToolsDockBar(QtGui.QWidget):
    '''
    classdocs
    '''

    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(ToolsDockBar, self).__init__(parent)
        
        #Slider and label
        layout= QtGui.QHBoxLayout()
        self.videoSlider=QtGui.QSlider(QtCore.Qt.Horizontal)
        layout.addWidget(self.videoSlider)
        self.timeLabel=QtGui.QLabel('N/A')
        layout.addWidget(self.timeLabel)
        self.nextTurnButton = QtGui.QPushButton("Next Turn")
        layout.addWidget(self.nextTurnButton)

        self.setLayout(layout)