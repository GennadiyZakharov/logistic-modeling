
from lgcore.lgabstractitem import LgAbstractItem

class LgPackage(LgAbstractItem):
    def __init__(self, parent=None, owner=None, caption='product', cost=0,  count=1, icon=':/penguin.png'):
        super(LgPackage, self).__init__(parent, owner, caption, cost)
        self.count = count
        self.icon = icon
             
    def __str__(self):
        return 'Package' + str(self.hashValue)
    
