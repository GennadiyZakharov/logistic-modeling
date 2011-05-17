
from lgcore.lgabstractitem import LgAbstractItem

class LgPackage(LgAbstractItem):
    def __init__(self, type, parent=None, owner=None, caption='product', cost=0, icon=':/penguin.png'):
        super(LgPackage, self).__init__(parent, owner, caption, cost)
        self.kind = 'Package'
        self.type = type
        self.icon = icon
             
    
