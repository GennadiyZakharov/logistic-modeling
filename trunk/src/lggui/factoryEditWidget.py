from PyQt4 import QtGui, QtCore

from lgcore.signals import *


class FactoryEditWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(FactoryEditWidget, self).__init__(parent)
        
        layout = QtGui.QGridLayout()
        
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.textEdited.connect(self.on_updateData)
        nameText = QtGui.QLabel('Factory name:')
        layout.addWidget(nameText,0,0)
        layout.addWidget(self.nameEdit,0,1)
         
        self.activateEdit = QtGui.QSpinBox()
        self.activateEdit.setMaximum(20)
        self.activateEdit.setValue(3)
        self.activateEdit.valueChanged.connect(self.on_updateData)
        activateText = QtGui.QLabel('Activation interval, turns: ')
        layout.addWidget(activateText,1,0)
        layout.addWidget(self.activateEdit,1,1)
        
        self.consumeEdit = QtGui.QSpinBox()
        self.consumeEdit.setMaximum(20)
        self.consumeEdit.valueChanged.connect(self.on_updateData)
        consumeText = QtGui.QLabel('Consumes: ')
        layout.addWidget(consumeText,2,0)
        layout.addWidget(self.consumeEdit,2,1)
        
        self.produceEdit = QtGui.QSpinBox()
        self.produceEdit.setMaximum(20)
        self.produceEdit.valueChanged.connect(self.on_updateData)
        produceText = QtGui.QLabel('Produce: ')
        layout.addWidget(produceText,3,0)
        layout.addWidget(self.produceEdit,3,1)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.setLayout(layout)
        
    def on_updateData(self):
        flag = (self.nameEdit.text()!='' and self.activateEdit.value()!=0 and
                (self.consumeEdit.value()!=0 or self.produceEdit.value()!=0))
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(flag)
