from PyQt4 import QtGui
from lgcore.signals import signalClicked, signalItemMoved, signalPackage
from lggui.dndmenuListwidget import DnDMenuListWidget
from lggui.dndtablewidget import DnDTableWidget
from lggui.packagelistitem import PackageListItem
from lggui.packagetableitem import PackageTableItem

class NodeWidget(QtGui.QDialog):
    def __init__(self, node, parent=None):
        super(NodeWidget, self).__init__(parent)
        
        self.node = node # This is link to core node, wich represents
            # all node functionality 
        
        self.setWindowTitle(self.node.name)
        self.setAcceptDrops(False)
        self.linksList = []
         
        inputLabel = QtGui.QLabel('Come:')
        outputLabel = QtGui.QLabel('Destination:')
        
        self.inputList = DnDMenuListWidget(self)
        self.connect(self.inputList, signalItemMoved, self.onPackageMoved)
        self.connect(self.inputList, signalPackage, self.onPackage)
        
        self.outputList = DnDTableWidget(self)
        self.connect(self.outputList, signalItemMoved, self.onPackageMoved)
        self.connect(self.outputList, signalPackage, self.onPackage)
        #self.connect(self.outputList, signalCellChanged, )
        
        inputLabel.setBuddy(self.inputList)
        outputLabel.setBuddy(self.outputList)
        storageLabel = QtGui.QLabel('Storage:')
        
        self.storageList = DnDMenuListWidget(self)
        self.connect(self.storageList, signalItemMoved, self.onPackageMoved)
        self.connect(self.storageList, signalPackage, self.onPackage)
        storageLabel.setBuddy(self.storageList)
        
        self.okBtn = QtGui.QPushButton('&Ok')
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
        
    def onUpdateLists(self):
        self.inputList.clear()
        self.storageList.clear()
        self.outputList.clear()
        for package in self.node.entered :
            self.inputList.addItem(PackageListItem(package))
            
        if self.node.storageCapacity == 0 :
            self.storageList.setEnabled(False)
        else :
            self.storageList.setEnabled(True)
            for package in self.node.storage :
                self.storageList.addItem(PackageListItem(package))
        
        if self.node.links == set() :
            self.outputList.setEnabled(False)
        else :
            self.outputList.setEnabled(True)
            self.outputList.setColumnCount(len(self.node.links))     
            linkNumber = 0
            names = []
            self.linksList = []
            maxCapacity = 0
            for link,packages in self.node.linksDict.items():
                names.append(link.name)
                self.linksList.append(link)
                maxCapacity = max(maxCapacity, link.maxCapacity)
                i=0
                for package in packages :
                    self.outputList.setItem(i,linkNumber,PackageTableItem(package))
                    i+=1
                linkNumber +=1
                
            self.outputList.setRowCount(maxCapacity)            
            self.outputList.setHorizontalHeaderLabels(names)
            
        self.onDistributionChanged()
    
    def onPackage(self, package, linkNumber=-1):
        if linkNumber >=0 :
            self.linkFrom = linkNumber
        if (self.source is self.target) and (self.source is not self.outputList) :
            self.onUpdateLists()  
            return
        if self.source is self.inputList :
            self.node.entered.discard(package)
            if self.target is self.storageList :
                self.node.storage.add(package)
            else : # target is table
                link = self.linksList[self.linkTo]
                self.node.linksDict[link].add(package)
                
        elif self.source is self.storageList :
            self.node.storage.discard(package)
            if self.target is self.inputList :
                self.node.entered.add(package)
            else : # target is table
                link = self.linksList[self.linkTo]
                self.node.linksDict[link].add(package)
        
        else : #source is table 
            link = self.linksList[self.linkFrom]
            self.node.linksDict[link].discard(package)
            if self.target is self.inputList :
                self.node.entered.add(package)
            elif self.target is self.storageList :
                self.node.storage.add(package)
            else : # table is source and target at same time
                    print 'move links'
                    print self.linkFrom, self.linkTo
                    link = self.linksList[self.linkTo]
                    self.node.linksDict[link].add(package)
                    
        
        self.onUpdateLists()
        
    
    def onPackageMoved(self, source, target, linkNumber=-1):
        self.source=source
        self.target=target
        if linkNumber >=0 :
            self.linkTo = linkNumber
    
    def onDistributionChanged(self):
        pass
        #self.okBtn.setEnabled(self.inputList.count() == 0)
        
        
        


        
