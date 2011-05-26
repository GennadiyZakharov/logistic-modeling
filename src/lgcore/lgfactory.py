from lgcore.lgabstractitem import LgAbstractItem
from lgcore.lgpackage import LgPackage

class  LgFactory(LgAbstractItem):
    '''
    classdocs
    '''

    def __init__(self, name='Forest', cost=0, parent=None, owner=None):
        '''
        Constructor
        '''
        super(LgFactory, self).__init__(name, parent, cost, owner)
        self.activationInterval = 3
        self.currentTurn = self.activationInterval 
        self.consumes = {}
        self.produce = {} 

    def execute(self, packagelist):
        # TODO: Add package type
        for i in range(self.consumes):
            packagelist.pop()
           
        for i in range(self.produce):
            packagelist.append(LgPackage(self.parent(), self.owner))

    def onNextTurn(self, packageList):
        super(LgFactory, self).onNextTurn()
        self.currentTurn -= 1
        if self.currentTurn == 0:
            self.currentTurn = self.activationInterval
            self.execute(packageList)
            
    
        
        
