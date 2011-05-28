from PyQt4 import QtGui
from lgcore.lgabstractitem import LgAbstractItem
from lgcore.signals import signalExecuteDialog, signalUpdateGui 

class LgNode(LgAbstractItem):
    '''
    This is class for logistic node. It can produce, consume and 
    distribute products for several links
    '''

    def __init__(self, name='Node', storageCapacity=0, parent=None, cost=0, owner=None ):
        super(LgNode, self).__init__(name, parent, cost, owner)
        self.kind = 'Node'      
        # List of links, to which product will be distributed
        self.links = set()
        
        # lists for all products
        self.entered = set() # products to be distributed
        self.storage = set() # storage to store products for a several time
        self.storageCapacity = storageCapacity
        self.factories = set()
        self.color = QtGui.QColor(195, 217, 255)
        # TEST:
        '''
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil', count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        '''
    def addLink(self, link):
        self.links.add(link)
        
    def delLink(self, link):
        self.links.remove(link)
        
    def produce(self):
        allpackages = self.entered | self.storage
        for factory in self.factories :
            factory.onNextTurn(allpackages)
            
        self.storage &= allpackages # in storage will be all packages, which was in storage before
        self.entered = allpackages - self.storage 
        
    def addFactory(self, factory):
        self.factories.add(factory)
        
    def removeFactory(self, factory):
        self.factories.remove(factory)
        
    def onNextTurn(self):
        super(LgNode, self).onNextTurn()
        self.produce()
        if len(self.entered) != 0 :
            self.emit(signalExecuteDialog)
        
    def onPackageEntered(self, package):
        self.entered.add(package)
        
    def onPropertiesChanged(self):
        self.emit(signalUpdateGui)
        
    def onMoved(self, pos):
        self.pos = pos
        
