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
        self.activationInterval = 1
        self.currentTurn = self.activationInterval 
        self.consumes = {}
        self.produces = {} 

    def execute(self, packagelist):
        # TODO: Add package type
        pass

    def onNextTurn(self, packageList):
        super(LgFactory, self).onNextTurn()
        self.currentTurn -= 1
        if self.currentTurn == 0:
            self.currentTurn = self.activationInterval
            self.execute(packageList)
            
    
        
        
