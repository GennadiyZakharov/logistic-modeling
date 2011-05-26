from PyQt4 import QtCore, QtGui

class FactoryListItem(QtGui.QListWidgetItem):
    '''
    classdocs
    '''
    


    def __init__(self, factory, parent=None):
        '''
        Constructor
        '''
        super(FactoryListItem, self).__init__(factory.name)
        self.factory = factory
        #self.setIcon(QtGui.QIcon())
