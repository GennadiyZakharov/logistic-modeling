from PyQt4 import QtGui, QtCore

from lgcore.signals import *
from lgcore.lgfactory import LgFactory


class FactoryEditWidget(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, factory=None, parent=None):
        '''
        Constructor
        '''
        super(FactoryEditWidget, self).__init__(parent)
        
        self.factory = factory if factory is not None else LgFactory()
        
        layout = QtGui.QGridLayout()
        
        self.nameEdit = QtGui.QLineEdit(self.factory.caption)
        self.nameEdit.textEdited.connect(self.onNameChanged)
        nameText = QtGui.QLabel('Factory name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText,0,0)
        layout.addWidget(self.nameEdit,0,1)
         
        self.activateEdit = QtGui.QSpinBox()
        self.activateEdit.setValue(self.factory.activationInterval)
        self.activateEdit.setMaximum(20)
        self.activateEdit.valueChanged.connect(self.onActivateChanged)
        activateText = QtGui.QLabel('Activation interval, turns: ')
        activateText.setBuddy(self.activateEdit)
        layout.addWidget(activateText,1,0)
        layout.addWidget(self.activateEdit,1,1)
        
        self.consumeEdit = QtGui.QSpinBox()
        self.consumeEdit.setValue(self.factory.consumes)
        self.consumeEdit.setMaximum(20)
        self.consumeEdit.valueChanged.connect(self.onConsumeChanged)
        consumeText = QtGui.QLabel('Consumes: ')
        layout.addWidget(consumeText,2,0)
        layout.addWidget(self.consumeEdit,2,1)
        
        self.produceEdit = QtGui.QSpinBox()
        self.produceEdit.setValue(self.factory.produce)
        self.produceEdit.setMaximum(20)
        self.produceEdit.valueChanged.connect(self.onProduceChanged)
        produceText = QtGui.QLabel('Produce: ')
        layout.addWidget(produceText,3,0)
        layout.addWidget(self.produceEdit,3,1)
        
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | 
                                           QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.setLayout(layout)
        
    def onNameChanged(self, text):
        self.factory.caption = text
        self.onUpdateData()
        
    def onActivateChanged(self, value):
        self.factory.activationInterval = value
        self.onUpdateData()
        
    def onConsumeChanged(self, value):
        self.factory.consumes = value
        self.onUpdateData()
        
    def onProduceChanged(self, value):
        self.factory.consumes = value
        self.onUpdateData()
        
    def onUpdateData(self):
        flag = (self.nameEdit.text()!='' and self.activateEdit.value()!=0 and
                (self.consumeEdit.value()!=0 or self.produceEdit.value()!=0))
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(flag)

