from lgcore.lgabstractitem import LgAbstractItem
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalCost
import random

class  LgFactory(LgAbstractItem):
    '''
    classdocs
    '''

    def __init__(self, name='Forest', cost=0, parent=None, owner=None):
        '''
        Constructor
        '''
        super(LgFactory, self).__init__(name, parent, cost, owner)
        self.activationInterval = 1
        self.currentTurn = self.activationInterval 
        self.consumes = {}
        self.produces = {}
        self.demands = {}
        self.income = 0 
        self.fee = 0

    def findPackages(self, name, count, packageSet):
        currentCount = 0
        packages = set()
        for package in packageSet :
            if package.name == name :
                currentCount += 1
                packages.add(package)
                if currentCount == count : 
                    return packages
        return None, count - currentCount
                

    def execute(self, packageSet):
        for name in self.demands.keys() :
            count = self.demands[name]
            packages, deficit = self.findPackages(name, count, packageSet)
            if packages is not None :
                packageSet -= packages
                self.emit(signalCost, +self.income*len(packages))
            else : self.emit(signalCost, -self.fee*deficit)
            
        for name in self.produces.keys() :
            mean, disp = self.produces[name]
            for i in range(int(random.gauss(mean, disp))) :
                package = LgPackage(name)
                packageSet.add(package)
            
    
    def setDemand(self):
        self.demands.clear()
        for name in self.consumes.keys() :
            mean, disp = self.consumes[name]
            self.demands[name] = int(random.gauss(mean, disp))

    def onNextTurn(self, packageList):
        super(LgFactory, self).onNextTurn()
        self.currentTurn -= 1
        if self.currentTurn == 0:
            self.currentTurn = self.activationInterval
            self.execute(packageList)
            self.setDemand()
            
    
        
        
