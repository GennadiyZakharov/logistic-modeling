
from PyQt4 import QtCore
from lgcore.signals import signalNextTurn

class LgScheme(QtCore.QObject):
    '''
    This is parent class for all lgItems
    It containes all lgItems, can manage, load and save them
    '''
    def __init__(self):
        super(LgScheme, self).__init__()
        
    def on_NextTurnPressed(self):
        self.emit(signalNextTurn)
    
    def openScheme(self):
        pass
    
    def saveScheme(self):
        pass
        
