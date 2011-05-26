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
        
        self.setWindowTitle('Edit factory properties')
        
        layout = QtGui.QGridLayout()
        
        self.nameEdit = QtGui.QLineEdit(self.factory.name)
        self.nameEdit.textEdited.connect(self.onNameChanged)
        nameText = QtGui.QLabel('Factory name:')
        nameText.setBuddy(self.nameEdit)
        layout.addWidget(nameText, 0, 0)
        layout.addWidget(self.nameEdit, 0, 1)
         
        self.activateEdit = QtGui.QSpinBox()
        self.activateEdit.setValue(self.factory.activationInterval)
        self.activateEdit.setMaximum(20)
        self.activateEdit.valueChanged.connect(self.onActivateChanged)
        activateText = QtGui.QLabel('Activation interval, turns: ')
        activateText.setBuddy(self.activateEdit)
        layout.addWidget(activateText, 1, 0)
        layout.addWidget(self.activateEdit, 1, 1)
        
        self.consumeEdit = QtGui.QTableWidget()
        consumeText = QtGui.QLabel('Consumes: ')
        layout.addWidget(consumeText, 2, 0)
        layout.addWidget(self.consumeEdit, 3, 0)
        self.consumeEdit.setColumnCount(3)
        self.updateTable(self.factory.consumes, self.consumeEdit)                             
        addRowButton = QtGui.QPushButton('Add row')
        addRowButton.clicked.connect(self.onAddRowConsume)
        layout.addWidget(addRowButton, 5, 0)
        delRowButton = QtGui.QPushButton('Delete row')
        delRowButton.clicked.connect(self.onDelRowConsume)
        layout.addWidget(delRowButton, 6, 0)
        
        self.produceEdit = QtGui.QTableWidget()
        produceText = QtGui.QLabel('Produces: ')
        layout.addWidget(produceText, 2, 1)
        layout.addWidget(self.produceEdit, 3, 1)
        self.produceEdit.setColumnCount(3)
        self.updateTable(self.factory.produces, self.produceEdit)                             
        addRowButton = QtGui.QPushButton('Add row')
        addRowButton.clicked.connect(self.onAddRowProduce)
        layout.addWidget(addRowButton, 5, 1)
        delRowButton = QtGui.QPushButton('Delete row')
        delRowButton.clicked.connect(self.onDelRowProduce)
        layout.addWidget(delRowButton, 6, 1)
        
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
         
    def addRow(self, table, name='Wood', mean=0, disp=0):
        i = table.rowCount()
        table.setRowCount(i + 1)
        table.setItem(i, 0, QtGui.QTableWidgetItem(name))
        meanSpinBox = QtGui.QSpinBox()
        dispSpinBox = QtGui.QSpinBox()
        meanSpinBox.valueChanged.connect(dispSpinBox.setMaximum)
        meanSpinBox.setMaximum(20)
        meanSpinBox.setValue(mean)
        dispSpinBox.setValue(disp)    
        table.setCellWidget(i, 1, meanSpinBox)
        table.setCellWidget(i, 2, dispSpinBox)
        
    def delRow(self, table):
        table.removeRow(self.consumeEdit.currentRow())
    
    def onAddRowConsume(self):
        self.addRow(self.consumeEdit)
        
    def onAddRowProduce(self):
        self.addRow(self.produceEdit)
        
    def onDelRowConsume(self):
        self.delRow(self.consumeEdit)
    
    def onDelRowProduce(self):
        self.delRow(self.produceEdit)
    
    def updateTable(self, dict, table):
        table.clear()
        for name in dict.keys() :
            mean, disp = dict[name]
            self.addRow(table, name, mean, disp)
            
    def updateProduceTable(self):
        self.consumeEdit.clear()
        for name in self.factory.consumes.keys() :
            mean, disp = self.factory.consumes[name]
            self.addRow(self.consumeEdit, name, mean, disp)
        
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

    def writeDictionary(self, table, dict):
        dict.clear()
        for row in range(table.rowCount()) :
            name = table.item(row, 0).text()
            if name == '' : continue
            meanSpinBox = table.cellWidget(row, 1)
            dispSpinBox = table.cellWidget(row, 2)
            dict[name] = (meanSpinBox.value(), dispSpinBox.value())

    def accept(self):
        self.writeDictionary(self.consumeEdit, self.factory.consumes)
        self.writeDictionary(self.produceEdit, self.factory.produces)
        return super(FactoryEditWidget, self).accept()
