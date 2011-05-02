from PyQt4 import QtGui
from qrc_resources import *

class PackageWidget(QtGui.QListWidgetItem):
    '''
    This is class for package. 
    It containes name, count and picture for
    '''

    def __init__(self, package):
                
        self.package = package
        self.caption = package.caption + ' ' + str(package.count)
        super(PackageWidget, self).__init__(package.caption)
        self.setIcon(QtGui.QIcon(package.icon))
        
        
        
        
        
        
        