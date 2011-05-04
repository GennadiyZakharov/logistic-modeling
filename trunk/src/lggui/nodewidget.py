from PyQt4 import QtGui
from lgcore.signals import signalClicked, signalItemMoved
from lggui.packagewidget import PackageWidget
from lggui.dndmenuListwidget import DnDMenuListWidget
from lggui.dndtablewidget import DnDTableWidget

class NodeWidget(QtGui.QDialog):
    def __init__(self, node, parent=None):
        super(NodeWidget, self).__init__(parent)
        
        self.node = node # This is link to core node, wich represents
            # all node functionality 
        
        self.setWindowTitle(self.node.caption)
         
        inputLabel = QtGui.QLabel('Come:')
        outputLabel = QtGui.QLabel('Destination:')
        
        self.inputList = DnDMenuListWidget(self)
        self.connect(self.inputList, signalItemMoved, self.on_distributionChanged)
        
        self.outputList = DnDTableWidget(self)
        self.connect(self.outputList, signalItemMoved, self.on_distributionChanged)
        #self.connect(self.outputList, signalCellChanged, )
        
        inputLabel.setBuddy(self.inputList)
        outputLabel.setBuddy(self.outputList)
        storageLabel = QtGui.QLabel('Storage:')
        
        self.storageList = DnDMenuListWidget(self)
        self.connect(self.storageList, signalItemMoved, self.on_distributionChanged)
        storageLabel.setBuddy(self.storageList)
        
        self.okBtn = QtGui.QPushButton('&OK')
        self.connect(self.okBtn, signalClicked, self.accept)
                      
        layout = QtGui.QGridLayout()
        layout.addWidget(inputLabel, 0, 0)
        layout.addWidget(outputLabel, 0, 1)
        layout.addWidget(self.inputList, 1, 0)
        layout.addWidget(self.outputList, 1, 1)
        
        layout.addWidget(storageLabel, 2, 0, 1, 2)
        layout.addWidget(self.storageList, 3, 0, 1, 2)
        layout.addWidget(self.okBtn, 4, 1)
        
        #vSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
       
        self.setLayout(layout)
        
        
        '''    
        for package in node.storage :
            item = PackageWidget(package)
            self.storageList.addItem(item)
        ''' 
        
    def on_Update(self):
        for package in self.node.entered :
            item = PackageWidget(package)
            self.inputList.addItem(item)
            
        if self.node.storageCapacity == 0 :
            self.storageList.setEnabled(False)
            for package in self.node.storage :
                item = PackageWidget(package)
                self.storageList.addItem(item)
        else :
            self.storageList.setEnabled(True)
        
        if self.node.links == [] :
            self.outputList.setEnabled(False)
        else :
            self.outputList.setEnabled(True)
            self.outputList.setColumnCount(len(self.node.links))
            captions = []
            maxCapacity = 0
            for link in self.node.links :
                captions.append(link.caption)
                maxCapacity = max(maxCapacity, link.maxCapacity)
            self.outputList.setRowCount(maxCapacity)            
            self.outputList.setHorizontalHeaderLabels(captions)
            
        self.on_distributionChanged()
    
    def on_distributionChanged(self):
        self.okBtn.setEnabled(self.inputList.count() == 0)
        
        
        


        
