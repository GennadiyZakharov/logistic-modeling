from lgcore.signals import signalNextTurn
from lgcore.lgpackage import LgPackage
from lgcore.lgabstractitem import LgAbstractItem

class LgNode(LgAbstractItem):
    '''
    This is class for logistic node. It can produce, consume and 
    distribute products for several links
    '''

    def __init__(self, scheme, caption='Node', storageCapacity=10, cost=0):
        super(LgNode, self).__init__(cost)
        
        self.caption = caption
        
        # List of links, to which product will be distributed
        self.links = []
        
        # lists for all products
        self.entered = [] # products to be distributed
        self.storage = [] # storage to store products for a several time
        self.storageCapacity = storageCapacity
        self.connect(scheme, signalNextTurn, self.on_NextTurn)
        
        # TEST:
        for i in range(5) :
            self.entered.append(LgPackage(count=i))
            self.storage.append(LgPackage(caption='Oil', count=i))
            #self.destination.append(LgPackage('Oil',count=i))
        
    def addLink(self, link):
        self.links.append(link)
        
    def on_NextTurn(self):
        super(LgNode, self).on_NextTurn()        
        
    def on_PackageEntered(self, package):
        self.entered.append(package)
        
