from PyQt4 import QtGui
from qrc_resources import *

class PackageTableItem(QtGui.QTableWidgetItem):
    '''
    This is class for package. 
    It containes name, count and picture for
    '''

    def __init__(self, package):
                
        self.package = package
        super(PackageTableItem, self).__init__(package.name)
        self.setIcon(QtGui.QIcon(package.icon))
