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
              
        # List of links, to which product will be distributed
        self.links = []
        
        # lists for all products
        self.entered = [] # products to be distributed
        self.storage = [] # storage to store products for a several time
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
        
    def produce(self):
        allpackages = self.entered + self.storage
        for factory in self.factories :
            factory.on_NextTurn(allpackages)
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn()
        self.produce()
        if self.entered != [] :
            self.emit(signalNextTurnNode)
        
    def on_PackageEntered(self, package):
        self.entered.append(package)
        
