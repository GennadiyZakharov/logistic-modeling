
from PyQt4 import QtCore

class LgPlayer(QtCore.QObject):
    '''
    classdocs
    '''


    def __init__(self, name, parent=None):
        '''
        Constructor
        '''
        super(LgPlayer, self).__init__(parent)
        self.name = name
        self.money = 1000
        
    def on_Cost(self, cost):
        # TODO: Change cost to negative
        self.money -= cost
        