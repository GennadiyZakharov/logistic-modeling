from PyQt4 import QtCore
from lgcore.signals import signalNextTurn

class LgScheme(QtCore.QObject):
    def __init__(self):
        super(LgScheme, self).__init__()
        
    def on_NextTurnPressed(self):
        self.emit(signalNextTurn)
        
