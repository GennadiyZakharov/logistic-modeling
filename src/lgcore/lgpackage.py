
from PyQt4 import QtGui
from lgcore.lgabstractitem import LgAbstractItem

class LgPackage(LgAbstractItem):
    def __init__(self, name='Wood', cost=0, parent=None, owner=None, icon=':/penguin.png'):
        super(LgPackage, self).__init__(name, parent, cost, owner)
        
        self.kind = 'Package'
        self.icon = icon
        self.color = QtGui.QColor(255, 255, 136)
        if owner is not None :
            self.setOwner(owner)
             
    
