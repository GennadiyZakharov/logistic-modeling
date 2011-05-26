from PyQt4 import QtGui, QtCore
from lgcore.lgfactory import LgFactory
from lgcore.signals import *



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
        
        self.nameEdit = QtGui.QLineEdit(self.factory.name)
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
        
        self.consumeEdit = QtGui.QTableWidget()
        consumeText = QtGui.QLabel('Consumes: ')
        layout.addWidget(consumeText,2,0)
        layout.addWidget(self.consumeEdit,3,0,1,2)
        #self.consumeEdit.cellChanged.connect(self.onConsumeChanged)
        
        #self.consumeEdit.setRowCount(10)
        self.consumeEdit.setColumnCount(3)
        #self.consumeEdit.se
        self.updateConsumeTable()
                                     
        addRowButton = QtGui.QPushButton('Add row')
        addRowButton.clicked.connect(self.onAddRow)
        layout.addWidget(addRowButton,4,0)
        delRowButton = QtGui.QPushButton('Delete row')
        delRowButton.clicked.connect(self.onDelRow)
        layout.addWidget(delRowButton,4,1)
        
        buttons = QtGui.QDialogButtonBox.Ok
        if factory is None :
            buttons |= QtGui.QDialogButtonBox.Cancel
        
        self.buttonBox = QtGui.QDialogButtonBox(buttons)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        self.connect(self.buttonBox, signalAccepted,
                     self.accept)
        self.connect(self.buttonBox, signalRejected,
                     self.reject)
        layout.addWidget(self.buttonBox, 10, 0, 1, 2)
        
        self.setLayout(layout)
         
    def onAddRow(self, name='Wood', mean=0, disp=0):
        i = self.consumeEdit.rowCount()
        self.consumeEdit.setRowCount(i+1)
        self.consumeEdit.setItem(i,0,QtGui.QTableWidgetItem(name))
        meanSpinBox = QtGui.QSpinBox()
        dispSpinBox = QtGui.QSpinBox()
        meanSpinBox.valueChanged.connect(dispSpinBox.setMaximum)
        meanSpinBox.setMaximum(20)
        meanSpinBox.setValue(mean)
        dispSpinBox.setValue(disp)    
        self.consumeEdit.setCellWidget(i,1,meanSpinBox)
        self.consumeEdit.setCellWidget(i,2,dispSpinBox)
        
        
    def onDelRow(self):
        self.consumeEdit.removeRow(self.consumeEdit.currentRow())
    
    def updateConsumeTable(self):
        self.consumeEdit.clear()
        for name in self.factory.consumes.keys() :
            mean,disp = self.factory.consumes[name]
            self.onAddRow(name, mean, disp)
        
    def onNameChanged(self, text):
        self.factory.caption = text
        self.onUpdateData()
        
    def onActivateChanged(self, value):
        self.factory.activationInterval = value
        self.onUpdateData()
        
    def onUpdateData(self):
        if self.nameEdit.text() == '' :
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
            return
        self.factory.name = self.nameEdit.text() 
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)

    def accept(self):
        self.factory.consumes.clear()
        for row in range(self.consumeEdit.rowCount()) :
            name = self.consumeEdit.item(row, 0).text()
            if name == '' : continue
            meanSpinBox = self.consumeEdit.cellWidget(row, 1)
            dispSpinBox = self.consumeEdit.cellWidget(row, 2)
            self.factory.consumes[name] = (meanSpinBox.value(),
                                                      dispSpinBox.value())
        return super(FactoryEditWidget, self).accept()
    def onProduceChanged(self, value):
        pass