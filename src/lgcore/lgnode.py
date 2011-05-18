from lgcore.signals import signalNextTurnNode
from lgcore.lgpackage import LgPackage
from lgcore.lgabstractitem import LgAbstractItem

class LgNode(LgAbstractItem):
    '''
    This is class for logistic node. It can produce, consume and 
    distribute products for several links
    '''

    def __init__(self, parent=None, owner=None, caption='Node', storageCapacity=10, cost=0):
        super(LgNode, self).__init__(parent, owner, caption, cost)
        self.kind = 'Node'      
        # List of links, to which product will be distributed
        self.links = []
        
        # lists for all products
        self.entered = set() # products to be distributed
        self.storage = set() # storage to store products for a several time
        self.storageCapacity = storageCapacity
        self.factories = set()
        
        # TEST:
        '''
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil', count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        '''
    def addLink(self, link):
        self.links.append(link)
        
    def delLink(self, link):
        self.links.remove(link)
        
    def produce(self):
        allpackages = self.entered | self.storage
        for factory in self.factories :
            factory.on_NextTurn(allpackages)
            
        self.storage &= allpackages # in storage will be all packages, which was in storage before
        self.entered = allpackages - self.storage 
        
    def addFactory(self, factory):
        self.factories.add(factory)
        
    def removeFactory(self, factory):
        self.factories.remove(factory)
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn()
        self.produce()
        if len(self.entered) != 0 :
            self.emit(signalNextTurnNode)
        
    def on_PackageEntered(self, package):
        self.entered.add(package)
        
