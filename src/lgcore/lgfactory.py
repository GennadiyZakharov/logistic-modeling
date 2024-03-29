from __future__ import division
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
        self.kind = 'Factory'
        self.currentTurn = self.activationInterval 
        self.consumes = {}
        self.produces = {}
        self.demands = {}
        self.income = 0 
        self.fee = 0

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
        return packages, currentCount        

    def execute(self, packageSet):
        print '=== Factory {0} executing'.format(self.name)
        koef = 1
        for name, count in self.demands.items() :
            packages, realCount = self.findPackages(name, count, packageSet)
            print 'consuming {0} packages of {1}'.format(realCount, name)
            self.emit(signalCost, +self.income * len(packages))
            packageSet -= packages
            deficit = count - realCount
            koef *= (realCount / count)
            if deficit > 0 :
                print 'Sending fee for {0} undelivered packages'.format(deficit)
                self.emit(signalCost, -self.fee * deficit)
        # Produce  
        if koef != 1 and len(self.produces) > 0 :
            print 'Attenuating produce by {0}'.format(koef)
        for name, (mean, disp) in self.produces.items() :
            count = int(koef * random.gauss(mean, disp))
            print 'Producing {0} packages of {1}'.format(count, name)
            for i in range(count) :
                package = LgPackage(name)
                packageSet.add(package)
                self.emit(signalCost, -self.cost)
            
    def setDemand(self):
        self.demands.clear()
        for name, (mean, disp) in self.consumes.items() :
            demandCount = max(0, int(random.gauss(mean, disp)))
            if demandCount > 0:
                self.demands[name] = demandCount

    def onNextTurn(self, packageList):
        super(LgFactory, self).onNextTurn()
        self.currentTurn -= 1
        if self.currentTurn == 0:
            self.currentTurn = self.activationInterval
            self.execute(packageList)
            self.setDemand()
            
    
        
        
