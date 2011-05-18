from PyQt4 import QtCore, QtGui

class PlayerListItem(QtGui.QListWidgetItem):
    '''
    classdocs
    '''
    


    def __init__(self, player, parent=None):
        '''
        Constructor
        '''
        super(PlayerListItem, self).__init__('{0:25} {1:25}'.format(
                                          player.name, player.money))
        self.player = player
        #self.setIcon(QtGui.QIcon())
        