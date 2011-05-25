from PyQt4 import QtGui
from qrc_resources import *

class PackageListItem(QtGui.QListWidgetItem):
    '''
    This is class for package. 
    It containes name, count and picture for
    '''

    def __init__(self, package):
                
        self.package = package
        super(PackageListItem, self).__init__(package.name)
        self.setIcon(QtGui.QIcon(package.icon))
        
        
        
        
        
        
        