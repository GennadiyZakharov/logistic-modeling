from PyQt4 import QtGui
from lgcore.lgabstractitem import LgAbstractItem
from lgcore.signals import signalExecuteDialog, signalUpdateGui, signalCost, \
    signalPlayerTurn

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
        self.linksDict = {}
        
        # lists for all products
        self.entered = set() # products to be distributed
        self.storage = set() # storage to store products for a several time
        self.storageCapacity = storageCapacity
        self.factories = set()
        self.color = QtGui.QColor(195, 217, 255)
        self.distributeList = {} # list of links to distribute products
        # TEST:
        '''
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil', count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        '''
    def addLink(self, link):
        self.links.add(link)
        self.linksDict[link]=set()
        self.distributeList.clear()
        
    def delLink(self, link):
        self.links.remove(link)
        del self.linksDict[link]
        self.distributeList.clear()
        
    def produce(self):
        allPackages = self.entered | self.storage
        for factory in self.factories :
            factory.onNextTurn(allPackages)
        
        self.storage &= allPackages # in storage will be all packages, 
                                    #which was in storage before and not consumed
        self.entered = allPackages - self.storage 
        
    def addFactory(self, factory):
        self.factories.add(factory)
        factory.setOwner(self.owner)
        
    def removeFactory(self, factory):
        self.factories.remove(factory)
        factory.setOwner(None)
        
    def onPackageEntered(self, package):
        self.entered.add(package)
               
    def onMoved(self, pos):
        self.pos = pos
        
    def getDemands(self):
        demands = {}
        for factory in self.factories :
            if factory is not None :
                demands.update(factory.demands)
        return demands
    
    def setOwner(self, owner=None):
        super(LgNode, self).setOwner(owner)
        if self.owner is not None :
            self.disconnect(self.owner, signalPlayerTurn, self.onPlayerTurn)
        self.owner = owner
        if self.owner is not None :
            self.connect(self.owner, signalPlayerTurn, self.onPlayerTurn)
    
    def findPackages(self, name, count, packageSet):
        '''
        Return list of packages from packageSet, matching name, not more than count
        '''
        currentCount = 0
        packages = set()
        for package in packageSet :
            if package.name == name :
                currentCount += 1
                packages.add(package)
                if currentCount == count : 
                    break
        return packages       
      
    def distibuteByList(self):
        for name,(link, count) in self.distributeList.items() :
            packages = self.findPackages(name, count, self.entered)
            for package in packages :
                if link.currentCapacity == 0 :
                    break
                self.entered.discard(package) 
                self.linksDict[link].add(package)
            
    
    def onPrepare(self):
        # distribute packages to links
        for link,packageSet in self.linksDict.items() :
            for package in packageSet :
                link.onAddPackage(package)
            packageSet.clear()
        # Moving rest of packages to storage
        while (len(self.storage) < self.storageCapacity) and (len(self.entered)>0) :
            self.storage.add(self.entered.pop())
        #clear packages 
        self.entered.clear()
        print 'node',self.name,'prepared'
        print self.linksDict
        
    def onNextTurn(self):
        self.emit(signalCost, -self.cost*len(self.storage))
        self.produce()
        self.distibuteByList()
        self.emit(signalUpdateGui)
    
    def onPlayerTurn(self):
        if len(self.entered) != 0 :
            self.emit(signalExecuteDialog)
    
    