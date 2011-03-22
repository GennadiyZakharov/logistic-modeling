from lgcore.signals import signalTransport, signalNextTurn, signalUpdateGui
from lgcore.lgabstractitem import LgAbstractItem
from lgcore.lgpackage import LgPackage

class LgLink(LgAbstractItem):
    '''This class implements all functionality for link '''

    def __init__(self, input, output, scheme, caption='Link', length=5, maxCapacity=5, cost=0):
        super(LgLink, self).__init__(cost)
        
        self.input = input
        self.output = output
        self.caption = caption
        self.length = length
        self.maxCapacity = maxCapacity
        self.currentCapacity = self.maxCapacity
        self.packages = {} # List for store packages
        
        self.input.addLink(self)
        
        self.connect(self.input, signalTransport, self.on_addPackage)
        self.connect(self, signalTransport, self.output.on_PackageEntered)
        self.connect(scheme, signalNextTurn, self.on_NextTurn)
        
        self.on_addPackage(LgPackage())
        
    def on_NextTurn(self):
        super(LgLink, self).on_NextTurn()
        for p in self.packages.keys():
            self.packages[p] -= 1
            if self.packages[p] == 0 :
                self.emit(signalTransport, self.packages.pop(p))
            # decrease by one age of good
        self.currentCapacity = self.maxCapacity
        self.emit(signalUpdateGui)
                
        
    def on_addPackage(self, package):
        '''Add new package to transport'''
        if self.currentCapacity > 0:
            self.packages[package] = self.length
            self.currentCapacity -= 1
            self.emit(signalUpdateGui)
        else:
            raise ValueError('Max capacity of link exceeded!')
        
        
