from hashlib import sha512
from time import time
from lgcore.lgabstractitem import LgAbstractItem

class LgPackage(LgAbstractItem):
    def __init__(self, cost=0, caption='product', count=1, icon=':/penguin.png'):
        super(LgPackage, self).__init__(cost)
        self.caption = caption
        self.count = count
        self.icon = icon
        self.hashValue = int(sha512(str(time())).hexdigest(), 16) 
        
    def __hash__(self):
        return self.hashValue
    
    def __str__(self):
        return 'Package' + str(self.hashValue)
    
